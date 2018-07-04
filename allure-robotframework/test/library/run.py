import os
import robot
from tempfile import mkdtemp
from multiprocessing import Process
from allure_robotframework import allure_robotframework
from allure_commons_test.report import AllureReport


def make_temp_dir():
    return mkdtemp(dir=os.environ.get('TEST_TMP', None))


def make_dir(path, name):
    dir_path = os.path.join(path, name)
    os.mkdir(dir_path)
    return dir_path


def make_file(path, name, content):
    file_path = os.path.join(path, name)
    with open(file_path, 'w+') as f:
        f.write('\n'.join(content))


def make_test_case(path, name, test_case):
    robot_file_path = os.path.join(path, name)
    with open(robot_file_path, 'w+') as robot_file:
        robot_file.write(test_case.replace('\n ', '\n'))
    return robot_file_path


def robot_run_with_allure(work_dir, *args, **kwargs):
    # ToDo: fix it (_core not works correctly with multiprocessing)
    import six
    import allure_commons
    if six.PY2:
        reload(allure_commons._core)
    else:
        import importlib
        importlib.reload(allure_commons._core)

    allure_dir = os.path.join(work_dir, 'allure')
    listener = allure_robotframework(logger_path=allure_dir)

    output_dir = os.path.join(work_dir, 'output')
    os.mkdir(output_dir)

    stdout_file = os.path.join(output_dir, 'stdout.txt')

    with open(stdout_file, 'w+') as stdout:
        options = {"listener": listener, "outputdir": output_dir, "stdout": stdout}
        options.update(kwargs)

        robot_process = Process(target=robot.run, args=args, kwargs=options)
        robot_process.start()
        robot_process.join()

    return AllureReport(allure_dir)

