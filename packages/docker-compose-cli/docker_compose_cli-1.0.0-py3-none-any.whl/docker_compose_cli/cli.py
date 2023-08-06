import logging
import os.path
from argparse import ArgumentParser
from distutils.sysconfig import get_python_lib
from logging import getLogger


logger = getLogger(__name__)
logger.setLevel(logging.INFO)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("app_name", default="app")
    return parser.parse_args()


def generate_dockerfile(args):
    path = os.path.join(
        get_python_lib(),
        "docker_compose_cli",
        "templates",
        "Dockerfile"
    )
    new_path = os.path.join(
        os.getcwd(),
        "Dockerfile"
    )
    if os.path.exists(new_path):
        logger.warning("Dockerfile already exists")
        return

    with open(path) as source_f:
        data = source_f.read()
        with open(new_path, 'w+') as dest_f:
            dest_f.write(data)


def generate_docker_compose_yml_file(args):
    path = os.path.join(
        get_python_lib(),
        "docker_compose_cli",
        "templates",
        "docker-compose.yml"
    )
    new_path = os.path.join(
        os.getcwd(),
        "docker-compose.yml"
    )
    if os.path.exists(new_path):
        logger.warning("docker-compose.yml already exists")
        return

    with open(path) as source_f:
        data = source_f.read()
        data = data.format(app_name=args.app_name)
        with open(new_path, 'w+') as dest_f:
            dest_f.write(data)


def generate_dot_env(args):
    new_path = os.path.join(
        os.getcwd(),
        ".env"
    )
    if os.path.exists(new_path):
        logger.warning(".env already exists.")
        return

    with open(new_path, 'w+'):
        ...


def main():
    args = parse_args()
    logger.info("Generating Dockerfile...")
    generate_dockerfile(args)
    logger.info("Generating docker-compose.yml file...")
    generate_docker_compose_yml_file(args)
    logger.info("Generating .env file...")
    generate_dot_env(args)
    logger.info("Done.")


if __name__ == '__main__':
    main()
