"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import logging

from app import app


if __name__ == "__main__":
    """
    Warning!: Development use only. Do not use on production.
    Start Gunicorn for production.
    """
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
    app.run(host="0.0.0.0", port=80, threaded=True)  # 80 For HTTP.
