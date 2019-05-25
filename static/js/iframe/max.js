$(function () {
			$('#supported').text('Supported/allowed: ' + !!screenfull.enabled);

			if (!screenfull.enabled) {
				return false;
			}

			$('#request').click(function () {
				screenfull.request($('#container')[0]).then(function () {
					console.log('Browser entered fullscreen mode')
				})
				
			});

			$('#exit').click(function () {
				screenfull.exit().then(function () {
					console.log('Browser exited fullscreen mode')
				});
			});

			$('#toggle').click(function () {
				screenfull.toggle($('#container')[0]).then(function () {
					console.log('Fullscreen mode: ' + (screenfull.isFullscreen ? 'enabled' : 'disabled'))
				});
			});
	
			
			$('.full-box').click(function () {
				screenfull.toggle($('.box')[0]);				
				
			});
			function fullscreenchange() {
				var elem = screenfull.element;

				$('#status').text('Is fullscreen: ' + screenfull.isFullscreen);

				if (elem) {
					$('#element').text('Element: ' + elem.localName + (elem.id ? '#' + elem.id : ''));
				}

				if (!screenfull.isFullscreen) {
					$('#external-iframe').remove();
					document.body.style.overflow = 'auto';
				}
			}

			screenfull.on('change', fullscreenchange);
			
			fullscreenchange();
		});