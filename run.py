
import os
from cashier_service import create_app


if __name__ == "__main__":
	create_app().run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
