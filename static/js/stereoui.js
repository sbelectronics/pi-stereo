COLORS = ["red", "green", "blue", "white", "magenta", "yellow", "cyan",  "black", "orange"];

function stereo() {
    onVolumeChange = function() {
        console.log("VolumeChange");
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
        //$("#now-playing-station-select").val("---")
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

    onInput = function(i) {
        var button_selector = "#input" + i;
        var icon_selector = "#icon-input" + i;
        $(".btn-input").removeClass("active");
        $(".icon-input").hide();
        $(button_selector).addClass("active");
        $(icon_selector).show()
        if (stereo.postUI) {
            stereo.setInput(i);
        }
    }

    onFMStation = function(i) {
        var button_selector = "#fmstation-" + i;
        var icon_selector = "#icon-fmstation-" + i;
        $(".btn-fmstation").removeClass("active");
        $(".icon-fmstation").hide();
        $(button_selector).addClass("active");
        $(icon_selector).show()
        if (stereo.postUI) {
            stereo.setFMStation(i);
        }
    }

    sendVolume = function(volume) {
        $.ajax({url: "/stereo/setVolume?volume=" + volume});
    }

    setPower = function(value) {
        $.ajax({url: "/stereo/setPower?value=" + value});
    }

    setInput = function(value) {
        $.ajax({url: "/stereo/setInput?value=" + value});
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

    setFMStation = function(value) {
        $.ajax({url: "/stereo/setFMStation?value=" + value});
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

        $("#input0").click(function() { stereo.onInput(0); } );
        $("#input1").click(function() { stereo.onInput(1); } );
        $("#input2").click(function() { stereo.onInput(2); } );
        $("#input3").click(function() { stereo.onInput(3); } );

        $("#fmstation-pandora").click(function() { stereo.onFMStation("pandora"); } );
        $("#fmstation-945").click(function() { stereo.onFMStation("945"); } );
        $("#fmstation-991").click(function() { stereo.onFMStation("991"); } );

        $("#love-song").click(function() { stereo.loveSong(); });
        $("#ban-song").click(function() { stereo.banSong(); });
    }

    updateStationComboBox = function(station, stations) {
        html = "";
        //html = '<option value="---">---</option>';

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

        if (stereo.didChosen) {
            $("#now-playing-station-select").trigger("chosen:updated");
        } else {
            $("#now-playing-station-select").chosen({disable_search: true});
            stereo.didChosen = true;
        }
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
                if (! $("#power-on").hasClass("active") ) {
                    $("#icon-power-on").click();
                }
            } else {
                if (! $("#power-off").hasClass("active") ) {
                    $("#icon-power-off").click();
                }
            }
            if (settings["song"]) {
                $("#now-playing-song").text(settings["song"]);
            }
            if (settings["artist"]) {
                $("#now-playing-artist").text(settings["artist"]);
            }
            if (settings["input"]) {
                onInput(settings["input"]);
            }
            if (settings["station"]) {
                //$("#now-playing-station").text(settings["station"]);

                if (this.lastStationName != settings["station"]) {
                    console.log("XXX");
                    this.lastStationName = settings["station"];
                    this.showedStationComboBox=true;
                    this.updateStationComboBox(settings["station"], settings["stations"]);
                }
            }
            if (settings["fmstation"]) {
                onFMStation(settings["fmstation"]);
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

