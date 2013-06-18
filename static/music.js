var curTs = 0;

function update_info()
{
  // Show station / track info
  $.get("info", function(data){
    if( ! 'ts' in data)
      return;
    if(data['ts'] == curTs)
      return;
    curTs = data['ts'];
    if('artist' in data)
      $("#music_artist").text(data["artist"]);
    if('title' in data)
      $("#music_track").text(data["title"]);
    if('album' in data)
      $("#music_album").text(data["album"]);
    if('detailUrl' in data)
      $("#music_link").attr('href', data["detailUrl"]);
    if('coverArt' in data)
      $("#music_art").attr('src', data["coverArt"]);
  });
}
    //Info 'artist', 'title', 'album', 'covertArt',
      //                             'stationName', 'detailUrl'

$(document).ready(function() {
  $("[rel=popover]").popover({'trigger':'hover'});

  $(".playpause").click(function(){$.get("pause");});

  $(".skip").click(function(){$.get("skip");});

  $(".vol_up").click(function(){$.get("volume/up");});

  $(".vol_down").click(function(){$.get("volume/down");});

  $(".refresh_stations").click(function(){$(location).attr('href','stations_refresh');});

  $(".restart_pianobar").click(function(){$.get("volume/down");});

  $(".station_link").click(function(){$.get("station/" + $(this).attr('rel'));});

  // Update track info every few seconds
  setInterval(function(){update_info();}, 7000);
});

