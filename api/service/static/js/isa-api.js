/**
 * Created by alfie on 20/05/15.
 */

IsaApi = {};

IsaApi.variables = {};

IsaApi.prototype = {
    init: function() {
        //IsaApi.prototype.isatabToIsajsonByFileCall();
    },

    isatabToIsajsonByFileCall: function() {
        $("#isatabToIsajsonByFileForm").on("submit", function() {
            event.preventDefault();
            // check if the user has chosen the file
            if ($("#inputIsatabFile").val() !== '') {
                $.ajax({
                    url: "/uploadIsatabByFile",
                    type: "POST",
                    data: new FormData(this),
                    async: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        alert(data)
                    }
                });
            } else {
                alert("Please enter either an ISA-TAB file (.zip).")
            }
        });
    },

    isatabToIsajsonByAccessionNumberCall: function() {
        $("isatabToIsajsonByAccessionNumberForm").on("submit", function() {
            event.preventDefault();
            // check if the user has chosen the file
            if ($("#inputIsatabAccessionNumber").val() !== '') {
                $.ajax({
                    url: "/uploadIsatabByAccessionNumber",
                    type: "POST",
                    data: new FormData(this),
                    async: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        alert(data)
                    }
                });
            } else {
                alert("Please enter either an ISA-TAB file (.zip).")
            }
        });
    }
};

IsaApi.prototype.init();
