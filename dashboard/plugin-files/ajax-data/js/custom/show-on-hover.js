/*------------------------------------------------------------
	ULTRA MENU INIT
	[Please read documentation for additional Information] 
--------------------------------------------------------------*/

// Strict Mode
'use strict';

// Ultra Menu Initialisation
function ultraMenuInit(){

	// Menu Init
	if($('.left-menu-wrapper').length){
		$('.left-menu-wrapper').ultraMenu({

            // Show on hover
            showHover: true,

			// Collapse Panel ON/OFF
            collapsePanel: true,

            // Panel Width Settings
            panelWidth: 240,
            collapsePanelWidth: 50,

            // JS based Offcanvas Effect
            offCanvas: true,
            offCanvasSpeed: 220,
            offCanvasClass: 'offcanvas-mode'

		});
	}
}

// Min Height Adjustment on Start (Required for better animations)
function adjustParameter() {
    var height = $(document).height();
    var boxed_view_set = 29; // Same as set in LESS Variables
    
    // Setting min-height via CSS (reqired)
    $("<style type='text/css'> #u-left-panel{ min-height: " + height +"px; } .content-panel{ min-height: " + (height - 80) +"px;} </style>").appendTo("head");

    var top_width = $(window).width() - 2*29;
    // Setting topbar min-width for(boxed && fixed mode)--
    $('#u-topbar').css('min-width', top_width);
}

$(document).ready(function() {
	//UltraMenu Init
	ultraMenuInit();

	// Adjust min height
	adjustParameter();

	// make code pretty
    window.prettyPrint && prettyPrint();
});
