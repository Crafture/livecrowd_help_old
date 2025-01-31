app.controller("faqCtrl", function(restService, $timeout) {
	/**
	 * Initial properties
	 */

	this.requestUrl = null;
	this.questions = null;
	this.filterCategory = null;
	this.filterQuestion = null;
	this.categories = [];
	this.standardCategories = [];
	this.standardVenuesEvents = [];
	this.eventInfo = null;
	this.showEventInfo = false;
	this.showMessage = false;
	this.edit = false;
	this.add = true;
	this.addEdit = {
		id : null,
		question : null,
		answer : null,
		category : null,
		event: null
	};

	/**
	 * methods of 'faqCtrl'
	 */

	this.initialize = function() {
		this.show = false;

		// Get first Venue/Event on screen by initalization
		var firstVenueOrEvent = document.querySelectorAll(".eventsOrVenues")[0];
		firstVenueOrEvent.classList.add("active");
		this.getQuestionsAndCategories(firstVenueOrEvent.dataset.url);
		this.getEventInfo();
	};

	this.getEventInfo = function() {
		var self = this;
		restService.get("/event-info-get" + this.requestUrl).then(function(data) {
			var data = JSON.parse(data);
			self.eventInfo = data[0];
			console.log(self.eventInfo);
		});
	};

	this.showEventInfoModal = function() {
		console.log(true);
		this.showEventInfo = true;
	};

	this.closeEventInfoModal = function() {
		this.showEventInfo = false;
	};

	this.getQuestionsAndCategories = function(venueOrEvent) {
		this.requestUrl = venueOrEvent;
		this.show = true;
		this.filterCategory = "";
		this.filterQuestion = "";
		var self = this;
		restService.get(this.requestUrl).then(function(data) {
			self.questions = JSON.parse(data);
			self.setCategories(self.questions);
			self.setShowAllActive();
		});
		this.getCategoriesAndVenuesEvents();
		this.getEventInfo();
		this.setCopyFramework();
	};

	/**
	 * sets the standard categories and venues/events
	 */
	
	this.getCategoriesAndVenuesEvents = function() {
		var self = this;
		restService.get("/categories-get/").then(function(data) {
			var data = JSON.parse(data);
			var categories = [];
			for (var i = 0; i < data.length; i++) {
				categories.push(data[i].fields.category);
			};
			self.standardCategories = _.uniq(categories);
		});

		restService.get("/events-get/").then(function(data) {
			var data = JSON.parse(data);
			var eventsVenues = [];
			for (var i = 0; i < data.length; i++) {
				eventsVenues.push(data[i].fields.event);
			};
			self.standardVenuesEvents = _.uniq(eventsVenues);
		});
	};

	/**
	 * set everytime the categories of an event/venue
	 */
	
	this.setCategories = function(questions) {
		this.categories = [];
		var arr = [];
		for (var i = 0; i < questions.length; i++) {
			arr.push(questions[i].fields.category);
		};
		this.categories = _.uniq(arr);
	};

	/**
	 * switches between categories and filters resultfield
	 */
	
	this.switchCategories = function(category) {
		this.filterCategory = category;
		this.filterQuestion = "";
		this.setCopyFramework();
	};

	/**
	 * shows all questions of event/venue
	 */
	
	this.showAll = function($event) {
		this.setActiveTab($event);
		this.filterCategory = "";
		this.filterQuestion = "";
		this.setCopyFramework();
	};

	/**
	 * sets 'Show All' a visually active state
	 */
	
	this.setShowAllActive = function() {
		var categories = document.querySelectorAll(".category");
		for (var i = 0; i < categories.length; i++) {
			categories[i].classList.remove("active");
		};

		document.querySelectorAll(".all")[0].classList.add("active");
	};

	/**
	 * copies a clicked question
	 */
	
	this.copyQuestion = function(questionId) {
		var self = this;
		restService.post("/" + questionId + "/count-plus/", $.param({
			pk : questionId
		})).then(function(response) {
			if(response.status === 200) {
				self.showMessage = true;
				self.message = response.data;
				self.showHideMessage();
			};
		});
	};

	/**
	 * initializes the copyframework:ClipboardJS on each element wich contains the className 'copy'
	 */
	
	this.setCopyFramework = function() {
		$timeout(function() {
			var btns = document.querySelectorAll('.copy');
			var clipboard = new ClipboardJS(btns);
		}, 2000);
	};

	/**
	 * sets tabs to active state
	 */
	
	this.setActiveTab = function($event) {
		var childsOfParentNodes = $event.currentTarget.parentNode.childNodes;
		for (var i = 0; i < childsOfParentNodes.length; i++) {
			if(typeof childsOfParentNodes[i].classList !== "undefined") {
				childsOfParentNodes[i].classList.remove("active");
			}
		};
		$event.currentTarget.classList.add("active");
	};

	/**
	 * add Edit Question methods
	 */
	
	this.editQuestion = function(question) {
		this.edit = true;
		this.add = false;

		this.addEdit = {
			id : question.pk,
			question : question.fields.question,
			answer : question.fields.answer,
			category : question.fields.category
		};
	};

	/**
	 * watch the changes of data in the AddEdit form ands sets add or edit state to the model
	 */
	
	this.watchAddEditForm = function() {
		if(this.edit == true && typeof this.addEdit.question === undefined && typeof this.addEdit.answer === undefined) {
			console.log(true);
			this.addEdit = {
				id : null,
				question : null,
				answer : null,
				category : null
			};
			this.edit = false;
			this.add = true;
		};
	};

	/**
	 * sends a POST request via AJAX to a new or edited question to a specific url
	 */
	this.sendQuestion = function($event) {
		$event.preventDefault();
		if(this.edit) {
			var self = this;
			restService.post("/question-update/" + self.addEdit.id + "/", $.param({
				pk: self.addEdit.id,
				question: self.addEdit.question,
				answer:	self.addEdit.answer,
				category: self.addEdit.category
			})).then(function(response) {
				if(response.status === 200) {
					self.showMessage = true;
					self.message = response.data;
					self.showHideMessage();
				};
			});
		};

		if(this.add) {
			var self = this;
			restService.post("/question-create/", $.param({
				question: self.addEdit.question,
				answer:	self.addEdit.answer,
				category: self.addEdit.category, 
				event: self.addEdit.event
			})).then(function(response) {
				if(response.status === 200) {
					self.showMessage = true;
					self.message = response.data;
					self.showHideMessage();
				};
			});
		};

		this.resetQuestion();
	};

	/**
	 * shows and hides a message
	 */
	this.showHideMessage = function() {
		var self = this;
		$timeout(function() {
			self.showMessage = false;
			self.message = null;
		}, 3000);
	};

	/**
	 * Resets the model and data of the addEdit form
	 */
	
	this.resetQuestion = function() {
		this.addEdit = {
			id : null,
			question : null,
			answer : null,
			category : null
		};
		this.edit = false;
		this.add = true;
	};

	/**
	 * Initializer of controller
	 */
	
	this.initialize();
});