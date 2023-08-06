import json
import os
import logging
from pathlib import Path
from .browser import Browser
from .imagetools import ImageTools
from .api import Api

log = logging.getLogger(f'vt.{os.path.basename(__file__)}')

class VisualTest:
    """
    Class for SmartBear VisualTest

    Args:
        driver: Selenium webdriver with active session
        settings: Dictionary of user settings
            - projectToken (str): Unique API token for your project. (required)
            - testRunName (str): Test Run Name - defaults to OS / Browser versions if not provided (optional)
            - saveTo (str): The directory to which images should be saved. (default is your working directory/results/)
        settings: Dictionary of developer settings
            - debugLogs (bool): Prints logs to stdout in addition to log file
            - debugImages (bool): Keeps temp folder of images used to build fullpage screenshots
            - saveDOM (bool): Saves DOM JSON file to same saveTo location
        limits: Dictionary of values to change default limits during creation fullpage images (not recommended)
            - MAX_IMAGE_PIXELS (int): Max fullpage image size. (default INT32 or 2^31)
            - MAX_TIME_MIN (float): Max time to create fullpage image.  Default is 3.5 minutes. Can be set to a max of 10 minutes. 
    Returns:
        Class instance
    """

    # imitate static variable across instances
    _consoleLogHandler = None

    def __init__(self, driver, settings: dict={}, limits: dict={}):
        log.info(f'Instantiated with settings: {settings}, limits: {limits}')

        # must do this first to get debug logs
        if 'debugLogs' in settings and type(settings['debugLogs']) == bool:
            self._handleLoggerSetting(settings['debugLogs'])

        self.browser = Browser(driver, limits)
        self._sessionId = driver.session_id
        self._settings = {
            'projectToken': None,
            'testRunName': None,
            'saveTo': None
        }

        # user-configurable project information
        if not 'projectToken' in settings:
            raise Exception('"projectToken" property in settings is required!')
        self._settings['projectToken'] = settings['projectToken']
        if 'testRunName' in settings:
            self._settings['testRunName'] = settings['testRunName']
        else:
            if self.browser._deviceInfo["osName"] == 'macos':
                osNamePretty = 'macOS'
            else:
                osNamePretty = self.browser._deviceInfo["osName"].capitalize()
            self._settings['testRunName'] = f'{osNamePretty} {self.browser._deviceInfo["osVersion"]} / {self.browser._deviceInfo["browserName"].capitalize()} {self.browser._deviceInfo["browserVersion"]}'

        if 'saveTo' in settings:
            self.saveTo = os.path.join(settings['saveTo'])
        else:
            self.saveTo = os.path.join(os.getcwd(),'results')
        
        if 'debugImages' in settings and type(settings['debugImages']) == bool:
            self.browser.debugImages = settings['debugImages']
        
        if 'saveDOM' in settings and type(settings['saveDOM']) == bool:
            self.browser.saveDOM = settings['saveDOM']
        
        # setup api
        self._api = Api(self._settings['projectToken'])
        
        log.info(f'final instance settings: {self._settings}')

    @property
    def projectToken(self):
        """
        Get projectToken (str)
        """
        return self._settings['projectToken']

    @property
    def saveTo(self):
        """
        Get/Set save directory path for screenshot results (str)
            - will create directories if path does not exist
        """
        return self._settings['saveTo']

    @saveTo.setter
    def saveTo(self, path):
        if type(path) == str:
            if not os.path.exists(path):
                tokens = os.path.split(path)
                try: 
                    os.makedirs(path)
                    self._settings['saveTo'] = path
                    log.info(f'Created new directory at {str(path)}')
                except Exception as e:
                    raise Exception(f'Error creating directory {str(path)}: {str(e)}')
            else:
                log.info(f'Directory already existed at: {path}')
                self._settings['saveTo'] = path
        else:
            raise Exception(f'Argument must be a string!')

    @property
    def scrollMethod(self):
        """
        Get/Set scrolling method for fullpage screenshots
        
        Args:
            method: name of scrolling method
                - CSS_TRANSLATE: default/recommended
                    - shifts the page up while capturing images but does not actually scroll the page
                - JS_SCROLL: not recommended
                    - uses Javascript to scroll the browser while capture images

        """
        return self.browser.scrollMethod

    @scrollMethod.setter
    def scrollMethod(self, method):
        self.browser.scrollMethod = method

    @property
    def capabilities(self):
        """
        Read-only access to selenium webdriver capabilities (dict)
        """
        return self.browser.capabilities

    @property
    def deviceInfo(self):
        """
        Read-only access to device info (dict)
        """
        return self.browser._deviceInfo

    @property
    def MAX_IMAGE_PIXELS(self):
        """
        Get/Set the maximum number of image pixels allowed for fullpage screenshot (int)
        """
        return ImageTools.getMaxImagePixels()

    @MAX_IMAGE_PIXELS.setter
    def MAX_IMAGE_PIXELS(self, pixels):
        ImageTools.setMaxImagePixels(pixels)

    @property
    def MAX_TIME_MIN(self):
        """
        Get/Set the current maximum number of minutes a fullpage screenshot is allowed to run before it stops scrolling (float)
        """
        return self.browser.MAX_TIME_MIN

    @MAX_TIME_MIN.setter
    def MAX_TIME_MIN(self, minutes):
        self.browser.MAX_TIME_MIN = minutes

    def _handleLoggerSetting(self, enableDebugLogs):
        ClassName = type(self)
        if enableDebugLogs == True:
            if ClassName._consoleLogHandler == None:
                logger = logging.getLogger('vt') #top-level logger created in __init__.py
                ClassName._consoleLogHandler = logging.StreamHandler()
                ClassName._consoleLogHandler.setFormatter(logging.Formatter('[VisualTesting][%(levelname)s] %(message)s'))
                logger.addHandler(ClassName._consoleLogHandler)
                logger.setLevel(logging.DEBUG)
        else:
            if ClassName._consoleLogHandler != None:
                logger = logging.getLogger('vt') #top-level logger created in __init__.py
                logger.removeHandler(ClassName._consoleLogHandler)

    def capture(self, name, options: dict={}):
        """
        Capture a screenshot from the browser under test
        
        Args:
            name: the unique name used both in naming the file, and identifying the visual test image 
            options: dictionary
                - { 'element': WebElement }: value must be a selenium webdriver element and will take an element screenshot
                - { 'vieport': true }: will capture an image of the browser's current viewport
                - if neither 'element', nor 'viewport' provided, defaults to capture a fullpage screenshot
                - { 'lazyload': 1000 }: For fullpage screenshot, will load lazy content before capturing screenshot
                - { 'ignoreElements': ['.css-selector'] }: For any screenshot, will specify elements to ignore during image comparison
        
        Returns:
            Information about the screenshot result
        """
        if not name:
            raise Exception(f'Name argument is required')

        if type(name) != str:
            raise Exception(f'Name argument must be a string')

        if len(name) > 100:
            raise Exception(f'Name argument cannot be greater than 100 characters')

        filePath = os.path.join(self._settings['saveTo'],f'{name}.png')
        imageType = None

        if 'ignoreElements' in options:
            if not isinstance(options['ignoreElements'], list):
                raise Exception(f'ignoreElements must be of type "list"')
            if not all(isinstance(item, str) for item in options['ignoreElements']):
                raise Exception(f'ignoreElements values must all be strings')
            
            elementsNotFound = []
            for cssSelector in options['ignoreElements']:
                try:
                    self.browser._findElement(cssSelector)
                except:
                    elementsNotFound.append(cssSelector)
            
            if len(elementsNotFound) > 0:
                raise Exception(f'Some ignoreElements were not found on the page: {",".join(elementsNotFound)}')
            else:
                self.browser._injectIgnoreElements(options['ignoreElements'])

        if 'element' in options:
            result = self.browser.takeElementScreenshot(options['element'], filePath)
            imageType = 'element'
        elif 'viewport' in options and options['viewport'] == True:
            result = self.browser.takeViewportScreenshot(filePath)
            imageType = 'viewport'
        else:
            if 'lazyload' in options:
                if type(options['lazyload']) != int or options['lazyload'] < 0 or options['lazyload'] > 10000:
                    raise Exception('"lazyload" value must be an integer between 0 and 10000 ms!')
                result = self.browser.takeFullpageScreenshot(filePath, options['lazyload'])
            else:
                result = self.browser.takeFullpageScreenshot(filePath)
            imageType = 'fullpage'
        
        # save image to server
        imageData = {
            'sessionId': self._sessionId,
            'imageName': name,
            'imageType': imageType,
            'imageExt': 'png',
            'testUrl': self.browser._driver.current_url,
            'viewportWidth': self.browser.viewportWidth,
            'viewportHeight': self.browser.viewportHeight,
            'imageWidth': result['imageSize']['width'],
            'imageHeight': result['imageSize']['height'],
            'dom': json.dumps(self.browser.dom),
            'ignoredElements': json.dumps(self.browser.dom['ignoredElementsData'])
        }
        imageData.update(self.browser._deviceInfo) # required information about device/os/browser

        # these two are informational and just used to store - not required
        imageData.update({'driverCapabilities': json.dumps(self.browser.capabilities)})
        imageData.update({'userAgentInfo': json.dumps(self.browser._userAgentInfo)})

        # post the image, creating testrun if new
        self._api.saveImage(self._settings['testRunName'], imageData, filePath)

        return result


