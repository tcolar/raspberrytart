$(document).ready(function() {
  $("[rel=popover]").popover({'trigger':'hover'});

  $(".playpause").click(function(){$.get("pause");});

  $(".skip").click(function(){$.get("skip");});

  $(".vol_up").click(function(){$.get("volume/up");});

  $(".vol_down").click(function(){$.get("volume/down");});

  $(".refresh_stations").click(function(){$(location).attr('href','stations_refresh');});

  $(".restart_pianobar").click(function(){$.get("volume/down");});

  $(".station_link").click(function(){$.get("station/" + $(this).attr('rel'));});

});

