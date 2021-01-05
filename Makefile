.PHONY: reinstall uninstall install

reinstall: uninstall install

uninstall:
	@echo Uninstalling central system...
	sudo rm -f /etc/systemd/system/gunicorn.service
	sudo rm -f /etc/systemd/system/gunicorn.socket
	sudo rm -f /usr/local/bin/central_system.sh
	sudo systemctl disable gunicorn
	sudo systemctl disable gunicorn.socket
	sudo systemctl stop gunicorn
	sudo systemctl stop gunicorn.socket
	sudo systemctl daemon-reload

install:
	@echo Installing AGV Database service...
	sudo cp service/gunicorn.* /etc/systemd/system/
	sudo cp service/central_system.sh /usr/local/bin/
	sudo systemctl daemon-reload
	sudo systemctl enable gunicorn
	sudo systemctl enable gunicorn.socket
	sudo systemctl start gunicorn
	sudo systemctl start gunicorn.socket

