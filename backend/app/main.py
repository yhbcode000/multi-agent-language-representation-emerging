import os
from app.dao.configDataManager import ConfigManager
from app.view.appView import AppView
from flask_cors import CORS
import sys

def main(working_dir='.'):
    # Change to the specified working directory
    os.chdir(working_dir)
    
    config_path = 'storage/config/main_config.yaml'
    config_manager = ConfigManager(config_path)
    flask_app_view = AppView(config_manager)
    flask_app = flask_app_view.app  # 获取Flask实例

    CORS(flask_app)  # 添加CORS支持

    flask_config_model = config_manager.config.flask
    flask_app.run(
        host=flask_config_model.host,
        port=flask_config_model.port,
        debug=flask_config_model.debug
    )


def run():
    # Check if a working directory is provided as a command-line argument
    if len(sys.argv) > 1:
        working_dir = sys.argv[1]  # Get the first argument as the working directory
    else:
        working_dir = '.'  # Default to the current directory if no argument is provided
    
    # Call main with the working directory argument
    main(working_dir)