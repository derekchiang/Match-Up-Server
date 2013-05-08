$(document).ready(function() {
	setTimeout(requestMatch, 100);

	$('#go-button').click(function(event) {
		var team_name = $('#team_name').val()
		var num_players = $('#num_players').val()
		jQuery.ajax({
			url: '//localhost:8000/',
			type: 'POST',
			data: {
				action: 'add',
				team_name: team_name,
				num_players: num_players
			},
			dataType: 'json',
			success: function(data, status, xhr) {
				$('#go').hide();
				$('#quit').show();
			},
			error: function(xhr, status, error) {
				alert("something went wrong: " + error);
            }
		});
	});

	$('#quit-button').click(function(event) {
		var team_name = $('#team_name').val()
		jQuery.ajax({
			url: '//localhost:8000/',
			type: 'POST',
			data: {
				action: 'remove',
				team_name: team_name
			},
			dataType: 'json',
			success: function(data, status, xhr) {
				$('#go').show();
				$('#quit').hide();
			}
		});
	});
});

function requestMatch() {
	var host = 'ws://localhost:8000/socket';
	var websocket = new WebSocket(host);
	websocket.onopen = function (evt) {};
	websocket.onmessage = function(evt) {
		setTimeout(function() {
			results = $.parseJSON(evt.data);
			$('#match').html("Your match is ready!! " + JSON.stringify(results));
			$('#quit').hide();
			$('#match').show();
		}, 100);
	};
	websocket.onerror = function (evt) {};
}