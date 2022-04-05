/*
 * View model for OctoPrint-Framer
 *
 * Author: Ricardo Riet Correa
 * License: GPLv3
 */
$(function() {
    function FramerViewModel(parameters) {
        var self = this;

        self.loginState = parameters[0];
        self.printerState = parameters[1];
        self.filesViewModel = parameters[2];
        self.temperatureState = parameters[3];

        self.initializeButton = function() {
            
			var buttonContainer = $('#job_print')[0].parentElement;
			buttonContainer.children[0].style.width = "100%";
			buttonContainer.children[0].style.marginBottom = "10px";
			buttonContainer.children[0].classList.remove("span4");
			buttonContainer.children[1].style.marginLeft = "0";

			self.btnFrame = document.createElement("button");
			self.btnFrame.id = "job_frame";
			self.btnFrame.classList.add("btn");
			self.btnFrame.classList.add("span4");
			self.btnFrame.addEventListener("click", self.btnFrameClick);

			self.btnFrameIcon = document.createElement("i");
			self.btnFrame.appendChild(self.btnFrameIcon);

			self.btnFrameText = document.createElement("span");
			self.btnFrame.appendChild(self.btnFrameText);

			self.btnFrameText.textContent = " Frame";
			self.btnFrameIcon.classList.add("fa", "fa-square-o");

			buttonContainer.appendChild(self.btnFrame);
		};

        self.btnFrameClick = function() {
            filePath = self.filesViewModel;
            $.ajax({
                url: API_BASEURL + "plugin/framer",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "frame"
                }),
                contentType: "application/json; charset=UTF-8",
                error: function (data, status) {

                    // Notification message
                    var options = {
                        title: "Frame failed.",
                        text: data.responseText,
                        hide: true,
                        buttons: {
                            sticker: false,
                            closer: true
                        },
                        type: "error"
                    };
                    // Send notification with the message above
                    new PNotify(options);
                }
            });
        };

        self.updateButton = function() {
            // disable the button if printer is not ready, is printing, user not logged in or file not selected.
			self.btnFrame.disabled = !self.temperatureState.isReady()
				|| self.temperatureState.isPrinting()
				|| !self.loginState.isUser()
				|| self.printerState.filename() == null;

		};

        // Check if the button should be enabled.
        self.butonStatus = function() {
            // Detect if the printer is not connected
            if (!this.printerState.isOperational()) {
                return false;
            }

            return true;
        }

        //self.onTabChange = function() { self.initializeButton(); };
        //self.onEventFileSelected = function() { self.initializeButton(); };
        
		self.initializeButton();
		self.fromCurrentData = function() { self.updateButton(); };
		self.updateButton();
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: FramerViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "loginStateViewModel", "printerStateViewModel", "filesViewModel", "temperatureViewModel"],
        // Elements to bind to, e.g. #settings_plugin_framer, #tab_plugin_framer, ...
        elements: [ /* ... */ ]
    });
});
