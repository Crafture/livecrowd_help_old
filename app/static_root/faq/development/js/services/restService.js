/**
 * restService for posting and getting data
 */

app.service('restService', function($http) {
	
	this.get = function(url) {
		return $http({
			url: url,
			method: "GET",
			contentType:'application/json'
		}).then(function(response){ 
			return response.data;
		});
	};

	this.post = function(url, data) {
		return $http({
				url: url, 
				method: "POST", 
				headers: { 
					'Content-Type' : 'application/x-www-form-urlencoded',
					'X-CSRFToken' : cookies['csrftoken']
				},
				data: data
			}).success(function(response) {
				return response;
			}).error(function(response) {
				return response;
			});
		};

});