COLORS = ["red", "green", "blue", "white", "magenta", "yellow", "cyan",  "black", "orange"];

function stereo() {
    onVolumeChange = function() {
        console.log("FPSChange");
        volume = $("#slider-volume").slider("value");
        $("#volume-setPoint").text(volume);
        if (stereo.postUI) {
            stereo.sendVolume(volume);
        }
    }

    onVolumeStartSlide = function() {
        console.log("startSlide");
        stereo.volumeSliding=true;
    }

    onVolumeStopSlide = function() {
        console.log("stopSlide");
        stereo.volumeSliding=false;
    }

    onPowerOn = function() {
        var button_selector = "#power-on";
        var icon_selector = "#icon-power-on";
        console.log("PowerOn");
        $(".btn-power").removeClass("active");
        $(".icon-power").hide();
        $(button_selector).addClass("active");
        $(icon_selector).show();
        if (stereo.postUI) {
            stereo.setPower(true);
        }
    }

    onPowerOff = function() {
        var button_selector = "#power-off";
        var icon_selector = "#icon-power-off";
        console.log("PowerOff");
        $(".btn-power").removeClass("active");
        $(".icon-power").hide();
        $(button_selector).addClass("active");
        $(icon_selector).show();
        if (stereo.postUI) {
            stereo.setPower(false);
        }
    }

    sendVolume = function(volume) {
        $.ajax({url: "/stereo/setVolume?volume=" + volume});
    }

    setPower = function(value) {
        $.ajax({url: "/stereo/setPower?value=" + value});
    }

    initButtons = function() {
        $("#slider-volume").slider({min: 1,
                                    max:2000,
                                    change: this.onVolumeChange,
                                    start: this.onVolumeStartSlide,
                                    stop: this.onVolumeStopSlide});

        $("#power-on").click(function() { stereo.onPowerOn(); });
        $("#power-off").click(function() { stereo.onPowerOff(); });
    }

    parseSettings = function(settings) {
        //console.log(settings);
        this.postUI = false;
        try {
            if ((!stereo.volumeSliding) && (!settings.volumeMoving)) {
                $("#slider-volume").slider({value: settings.volumeCurrent});
            }
            if (settings.volumeMoving) {
                $("#volume-moving").text(" (moving: " + settings.volumeCurrent + ")");
            } else {
                $("#volume-moving").text("");
            }
            if (settings["power"]) {
                $("#icon-power-on").click();
            } else {
                $("#icon-power-off").click();
            }
        }
        finally {
            this.postUI = true;
        }
    }

    requestSettings = function() {
        $.ajax({
            url: "/stereo/getSettings",
            dataType : 'json',
            type : 'GET',
            success: function(newData) {
                stereo.parseSettings(newData);
                setTimeout("stereo.requestSettings();", 1000);
            },
            error: function() {
                console.log("error retrieving settings");
                setTimeout("stereo.requestSettings();", 5000);
            }
        });
    }

    start = function() {
         this.postUI = true;
         this.initButtons();
         this.requestSettings();
    }

    return this;
}

$(document).ready(function(){
    stereo = stereo()
    stereo.start();
});

