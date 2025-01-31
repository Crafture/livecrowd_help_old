app.controller("faqCtrl", function(restService, $timeout) {
	/**
	 * Initial properties
	 */

	this.requestUrl = null;
	this.requestUrlBundle = [];
	this.weeklyUpdate = null;
	this.questions = null;
	this.filterCategory = null;
	this.filterQuestion = null;
	this.categories = [];
	this.standardCategories = [];
	this.standardVenuesEvents = [];
	this.selectAll = false;
	this.eventInfo = null;
	this.showWeeklyUpdate = false;
	this.showEventInfo = false;
	this.showMessage = false;
	this.addEditModal = false;
	this.questionInfoModal = false;
	this.questionInfoModalData = null;
	this.edit = false;
	this.add = true;
	this.archive = false;
	this.delete = false;
	this.firstTime = true;
	this.loader = false;
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

		// select all Venues/Events on screen by initalization
		this.setClientUrl();
		// this.selectAllVenuesAndEvents();
		this.getWeeklyUpdate();
		this.checkWeeklyUpdateReaded();
	};

	/**
	 * set client url
	 */

	this.setClientUrl = function() {
		this.requestUrl = document.querySelector('#client-nav a.active').dataset.url;
	};

	/**
	 * get client url
	 */

	this.getClientUrl = function() {
		return document.querySelector('#client-nav a.active').dataset.url;
	};

	/**
	 * get client post url
	 */

	this.getClientPostUrl = function() {
		return document.querySelector('#client-nav a.active').href;
	};

	/**
	 * check if weekly update is readed by cookie
	 */

	this.checkWeeklyUpdateReaded = function() {
		var readed = this.getCookie("readed");
		console.log(readed);
		if(this.getCookie("readed") === null) {
			this.readedWeeklyUpdate = false;
		} else {
			this.readedWeeklyUpdate = true;
			this.selectAllVenuesAndEvents();
		};
	};

	/**
	 * get cookie from the browser
	 */

	this.getCookie = function(name) {
		var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
		return v ? v[2] : null;
	};

	/**
	 * set cookie inside the browser
	 */	

	this.setReadedWeeklyUpdate = function() {
		document.cookie = "readed=true";
	};

	/**
	 * get weekly update by ajax
	 */	

	this.getWeeklyUpdate = function() {
		this.loader = true;
		var self = this;
		restService.get(this.getClientPostUrl() + "update/").then(function(data) {
			self.weeklyUpdate = JSON.parse(data);
			if(self.weeklyUpdate.length === 0) {
				self.show = true;
				self.selectAllVenuesAndEvents();
			};
			self.loader = false;
		});
	};

	/**
	 * sets first configuration ten questions
	 */	

	this.renderFirstTen = function() {
		this.questions.length = 10;
	};

	/**
	 * sets first configuration ten questions
	 */	

	this.setFirstTime = function() {
		if(this.firstTime) {
			this.renderFirstTen();
			this.firstTime = false;
		};
	};	

	/**
	 * gets data about the event/venue
	 */	

	this.getEventInfo = function() {
		var self = this;
		restService.get("/event-info-get/?" + this.setRequestUrl()).then(function(data) {
			var response = JSON.parse(data);
			self.eventInfo = response;
		});
	};

	/**
	 * shows modal/popup about the weekly update
	 */	
	
	this.showWeeklyUpdateModal = function() {
		this.showWeeklyUpdate = true;
	};

	/**
	 * closes modal/popup about the weekly update
	 */	
	
	this.closeWeeklyUpdateModal = function() {
		this.showWeeklyUpdate = false;
	};

	/**
	 * shows modal/popup about the event/venue
	 */	
	
	this.showEventInfoModal = function() {
		this.showEventInfo = true;
	};

	/**
	 * closes modal/popup about the event/venue
	 */	
	
	this.closeEventInfoModal = function() {
		this.showEventInfo = false;
	};

	/**
	 * set request url
	 */
	
	this.setRequestUrl = function(venueOrEvent) {
		var index = this.requestUrlBundle.indexOf(venueOrEvent);

		// IF venueOrEvent exists in the collection, remove it. ELSE add to url
		if(index !== -1) {
			this.requestUrlBundle.splice(index, 1);
		} else {
			this.requestUrlBundle.push(venueOrEvent);
			this.requestUrlBundle = _.uniq(this.requestUrlBundle);
		};
		
		var url = this.requestUrlBundle.join("&");
		return url;
	};

	/**
	 * set all elements in active state
	 */

	this.setAllElementsActive = function(element) {
		var elements = document.querySelectorAll(element);
		for (var i = 0; i < elements.length; i++) {
			elements[i].classList.add("active");
		};
	};

	/**
	 * unset all elements from active state
	 */

	this.unsetAllElementsActive = function(element) {
		var elements = document.querySelectorAll(element);
		for (var i = 0; i < elements.length; i++) {
			elements[i].classList.remove("active");
		};

	};

	/**
	 * get all queries to make an ajaxcall
	 */

	this.getAllQueries = function() {
		this.requestUrlBundle = [];
		this.requestUrl = this.getClientUrl();

		var events = document.querySelectorAll(".eventsOrVenues");
		for (var i = 0; i < events.length; i++) {
			this.requestUrlBundle.push(events[i].dataset.url);
		};
		this.requestUrlBundle = _.uniq(this.requestUrlBundle);
		this.requestUrl += "?" + this.requestUrlBundle.join("&");
	};

	/**
	 * select all events and venues and shows the resultlist
	 */

	this.selectAllVenuesAndEvents = function() {

		if(this.firstTime) {
			this.selectAll = false;
			this.getAllQueries();
			this.show = true;
			this.filterCategory = "";
			this.filterQuestion = "";
			this.loader = true;
			var self = this;
			restService.get(this.requestUrl).then(function(data) {
				self.questions = JSON.parse(data);
				self.loader = false;
				self.setCategories(self.questions);
				self.setShowAllActive();
				self.getEventInfo();
				self.setFirstTime();
				self.requestUrlBundle = [];
			});
			this.getCategoriesAndVenuesEvents();
			this.setCopyFramework();
		} else {
			if(!this.selectAll) {
				this.selectAll = true;
				this.setAllElementsActive(".selectall");
				this.setAllElementsActive(".venue");
				this.setAllElementsActive(".eventsOrVenues");

				this.getAllQueries();
				this.show = true;
				this.filterCategory = "";
				this.filterQuestion = "";
				this.loader = true;
				var self = this;
				restService.get(this.requestUrl).then(function(data) {
					self.questions = JSON.parse(data);
					self.loader = false;
					self.setCategories(self.questions);
					self.setShowAllActive();
					self.getEventInfo();
				});
				this.getCategoriesAndVenuesEvents();
				this.setCopyFramework();
			} else {
				this.selectAll = false;
				this.unsetAllElementsActive(".selectall");
				this.unsetAllElementsActive(".venue");
				this.unsetAllElementsActive(".eventsOrVenues");
				this.show = true;
				this.filterCategory = "";
				this.filterQuestion = "";
				this.requestUrlBundle = [];
				this.requestUrl = this.getClientUrl();
				this.questions = [];
				this.categories = [];
				this.setShowAllActive();
			};
		};
	};

	/**
	 * deselect select all element
	 */

	this.deselectAll = function() {
		this.selectAll = false;
		this.unsetAllElementsActive(".selectall");
	};

	/**
	 * deselect venue
	 */

	this.deselectVenue = function(element) {
		document.querySelector("a[data-venue='" + element.currentTarget.dataset.venueChild + "']").classList.remove("active");
	};

	/**
	 * toggle all venues
	 */

	this.toggleAllVenues = function(parent) {
		this.deselectAll();
		var events = document.querySelectorAll("a[data-venue-child='" + parent.currentTarget.dataset.venue + "']");
		if(parent.currentTarget.classList.contains("active")) {
			this.setAllElementsActive("a[data-venue-child='" + parent.currentTarget.dataset.venue + "']");

			for (var i = 0; i < events.length; i++) {
				this.requestUrlBundle.push(events[i].dataset.url);
			};

			this.requestUrlBundle = _.uniq(this.requestUrlBundle);
			this.setClientUrl();
			this.requestUrl += "?" + this.requestUrlBundle.join("&");
			this.show = true;
			this.loader = true;
			this.filterCategory = "";
			this.filterQuestion = "";


			var self = this;
			restService.get(this.requestUrl).then(function(data) {
				self.questions = JSON.parse(data);
				self.setCategories(self.questions);
				self.setShowAllActive();
				self.loader = false;
			});
			
			this.getCategoriesAndVenuesEvents();
			this.setCopyFramework();
			this.getEventInfo();
		} else {
			this.unsetAllElementsActive("a[data-venue-child='" + parent.currentTarget.dataset.venue + "']");

			for (var i = 0; i < events.length; i++) {
				var index = this.requestUrlBundle.indexOf(events[i].dataset.eventPk);

				// IF venueOrEvent exists in the collection, remove it. ELSE add to url
				if(index !== -1) {
					this.requestUrlBundle.splice(index, 1);
				};
			};

			this.requestUrlBundle = _.uniq(this.requestUrlBundle);
			this.setClientUrl();
			this.requestUrl += "?" + this.requestUrlBundle.join("&");

			this.show = true;
			this.loader = true;
			this.filterCategory = "";
			this.filterQuestion = "";

			var self = this;
			restService.get(this.requestUrl).then(function(data) {
				self.questions = JSON.parse(data);
				self.setCategories(self.questions);
				self.setShowAllActive();
				self.loader = false;
			});
			this.getCategoriesAndVenuesEvents();
			this.setCopyFramework();
			this.getEventInfo();
		};
	};

	/**
	 * gets the questions and categories based on venue/event
	 */	

	this.getQuestionsAndCategories = function(venueOrEvent) {
		this.deselectAll();
		this.setRequestUrl();

		this.setClientUrl();
		this.requestUrl += "?" + this.setRequestUrl(venueOrEvent);
		this.show = true;
		this.loader = true;
		this.filterCategory = "";
		this.filterQuestion = "";

		var self = this;
		restService.get(this.requestUrl).then(function(data) {
			self.questions = JSON.parse(data);
			self.setCategories(self.questions);
			self.setShowAllActive();
			self.loader = false;
		});
		this.getCategoriesAndVenuesEvents();
		this.setCopyFramework();
		this.getEventInfo();
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
				self.message = "Copied question";
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
			};
		};

		$event.currentTarget.classList.add("active");
	};

	/**
	 * sets navigation to active or inactive state
	 */

	this.setNavigationActive = function($event) {

		if($event.currentTarget.classList.contains("active")) {
			$event.currentTarget.classList.remove("active");
		} else {
			$event.currentTarget.classList.add("active");
		};
	};

	/**
	 * show Modal for addEdit questions
	 */

	this.showAddEditModal = function() {
		this.addEditModal = true;
		this.edit = false;
		this.add = true;
		this.addEdit = null;

	};

	/**
	 * show Modal for addEdit questions
	 */

	this.closeAddEditModal = function() {
		this.addEditModal = false;
	};

	/**
	 * add Edit Question methods
	 */
	
	this.editQuestion = function(question) {

		this.addEditModal = true;
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
	 * show Modal for addEdit questions
	 */

	this.showQuestionInfoModal = function() {
		this.questionInfoModal = true;
		this.setCopyFramework();

	};

	/**
	 * show Modal for addEdit questions
	 */

	this.closeQuestionInfoModal = function() {
		this.questionInfoModal = false;
		this.questionInfoModalData = null;
	};

	/**
	  * read info about question to copy to customers
	  */

	this.seeQuestionInfo = function(question, $index) {
		this.showQuestionInfoModal();
		this.questionInfoModalData = question;
	};

	/**
	 * watch the changes of data in the AddEdit form ands sets add or edit state to the model
	 */
	
	this.watchAddEditForm = function() {
		if(this.edit == true && typeof this.addEdit.question === undefined && typeof this.addEdit.answer === undefined) {
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
	 * sets edit modal state to archive
	 */

	this.archiveQuestion = function() {
		this.archive = true;
		this.delete = false;
	};

	/**
	 * sets edit modal state to delete
	 */

	this.deleteQuestion = function() {
		this.delete = true;
		this.archive = false;
	};

	/**
	 * sends a POST request via AJAX to a new or edited question to a specific url
	 */
	this.sendQuestion = function($event) {
		$event.preventDefault();

		var postUrl = this.getClientPostUrl();
		console.log(postUrl);

		if(this.edit) {

			var url;

			if(this.edit && !this.archive && !this.delete) {
				url = postUrl + "question-update/";
			} else if(this.edit && this.archive && !this.delete) {
				url = postUrl + "question-archive/";
			} else if(this.edit && !this.archive && this.delete) {
				url = postUrl + "question-delete/";
			};

			this.archive = false;
			this.delete = false;

			console.log(url);

			var self = this;
			restService.post(url + self.addEdit.id + "/", $.param({
				pk: self.addEdit.id,
				question: self.addEdit.question,
				answer:	self.addEdit.answer,
				category: self.addEdit.category
			})).then(function(response) {
				if(response.status === 200) {
					self.showMessage = true;
					self.message = "Succesfully send";
					self.showHideMessage();	
					self.syncData();
					self.viewLoader();
				};
			});
		};

		if(this.add) {
			var self = this;
			restService.post(postUrl + "question-create/", $.param({
				question: self.addEdit.question,
				answer:	self.addEdit.answer,
				category: self.addEdit.category, 
				event: self.addEdit.event
			})).then(function(response) {
				if(response.status === 200) {
					self.showMessage = true;
					self.message = "Succesfully send";
					self.showHideMessage();
					self.syncData();
					self.viewLoader();
				};	
			});
		};

		this.resetQuestion();
	};

	/**
	 * sync all questions data
	 */

	this.syncData = function() {
		var self = this;
		restService.get(this.requestUrl).then(function(data) {
			self.questions = JSON.parse(data);
		});
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
	 * shows loader
	 */
	
	this.viewLoader = function() {
		this.loader = true;
		var self = this;
		$timeout(function() {
			self.loader = false;
		}, 1000);
	};

	/**
	 * resets the model and data of the addEdit form
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
		this.closeAddEditModal();
	};

	/**
	 * initializer of controller
	 */
	
	this.initialize();
});