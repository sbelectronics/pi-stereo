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

    onStationChanged = function() {
        console.log("stationChanged");
        station_id = $("#now-playing-station-select").val();
        $("#now-playing-station-select").val("---")
        if (stereo.postUI) {
            stereo.setStation(station_id);
        }
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

    nextSong = function(value) {
        $.ajax({url: "/stereo/nextSong"});
    }

    loveSong = function(value) {
        $.ajax({url: "/stereo/loveSong"});
    }

    banSong = function(value) {
        $.ajax({url: "/stereo/banSong"});
    }

    setStation = function(value) {
        $.ajax({url: "/stereo/setStation?value=" + value});
    }

    initButtons = function() {
        $("#slider-volume").slider({min: 1,
                                    max:1625,
                                    change: this.onVolumeChange,
                                    start: this.onVolumeStartSlide,
                                    stop: this.onVolumeStopSlide});

        $("#power-on").click(function() { stereo.onPowerOn(); });
        $("#power-off").click(function() { stereo.onPowerOff(); });
        $("#next-song").click(function() { stereo.nextSong(); });

        $("#love-song").click(function() { stereo.loveSong(); });
        $("#ban-song").click(function() { stereo.banSong(); });
    }

    updateStationComboBox = function(station, stations) {
        html = '<option value="---">---</option>';

        for (k in stations) {
           station_num = stations[k][0];
           station_name = stations[k][1];
           selected="";

           if (station_name == station) {
               selected = " selected";
           } else {
               selected = "";
           }

           html = html + "<option value=" + station_num + selected + ">" + station_name + "</option>";
        }

        $("#now-playing-station-select").html(html);
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
            if (settings["song"]) {
                $("#now-playing-song").text(settings["song"]);
            }
            if (settings["artist"]) {
                $("#now-playing-artist").text(settings["artist"]);
            }
            if (settings["station"]) {
                //$("#now-playing-station").text(settings["station"]);

                if (this.lastStationName != settings["station"]) {
                    this.lastStationName = settings["station"];
                    this.showedStationComboBox=true;
                    this.updateStationComboBox(settings["station"], settings["stations"]);
                }
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

