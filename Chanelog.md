# Changelog livecrowd.help
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added

### Changed

## [0.2.1] - 2019-02-05
### Added

- Weekly update button with modal popup to display the latest update 

### Changed

- Only Admins can upload questions now from the main application
- Select all button not preselected from an initial load
- Weekly message only getting showed once
- Updating a question now supports categories and events
- Info button is by default gray and unclickable when there is no information about the question and blue when there is

## [0.2.0] - 2019-01-04
### Added
- Client Model
- Client Views
- Popup Elements
- Ajaxcall for questions /get/
- Filters
- Event Info Modal
- Question Delete and Archive 

### Changed
- Fixed error in Queryset
- Event info row to supernote
- Implemented latest versions for frontend
- fixed double quotes in templates to single quotes
- Fixed bug in question update

## [0.1.2.alpha] - 2019-01-04
#### Added
- Client Model
- Client Views
- Popup Elements
- Ajaxcall for questions /get/
- Filters
- Event Info Modal
- Question Delete and Archive 

### Changed
- Fixed error in Queryset
- Event info row to supernote
- Implemented latest versions for frontend
- fixed double quotes in templates to single quotes
- Fixed bug in question update

## [0.1.1] - 2018-05-04
#### Added
- Popup component for latest updates

### Changed
- Question model added archive row

## [0.1.0] - 2018-07-03
#### Added
- Multiple selection questions
- Created parent model with question
- Archive Feature

### Changed
- local.py changes
- fixed iframe error
- faq.html template changes
- sidebar


## [0.0.4.staging] - 2018-05-04
#### Added
- allowed hosts
- production settings 
- static root
- WSGI editor
- Footer
- admin.css

### Changed
- extended add/edit functionality with multi options
- .gitignore

## [0.0.3.alpha] - 2018-04-23
#### Added
- Categories-get query : fetch the categories
- EventGet query : fetch the events
- Created relationship between Event and Questions
- Eventinfo model
- GetEventInfo query: fetch the latest event info
- Responsive html

### Changed
- QuestionUpdate view 
- requirements.txt


## [0.0.2.alpha] - 2018-04-17
#### Added
- Html queries
- Upload Image files
- Faq Template
- Javascript AJAX with JSON parsing
- Favicon
- Admin Models
- Question Edit functionality
- Count Functionality
- Question Add functionality

### Changed
- Fixed Export to xlsx and csv
- Requirements.txt
- Login template
- Order questions by query fixed

## [0.0.1.alpha] - 2018-03-29
### Added
- Created django app folder
- Added readme
- Created Base Models
- Created django app folder
- Added readme
- Django-import-export implementation

### Changed
- Added changes to readme.md



