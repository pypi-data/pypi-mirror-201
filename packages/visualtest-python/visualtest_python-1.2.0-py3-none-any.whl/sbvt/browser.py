import os
import time
import shutil
import math
import logging
import json
from .imagetools import ImageTools
from .timer import StopWatch
from .api import Api
from selenium.webdriver.common.by import By

log = logging.getLogger(f'vt.{os.path.basename(__file__)}')

# defaults - can be overridden with limits parameter
DEFAULT_MAX_IMAGE_SIZE_MB = 20  # 20MB
DEFAULT_MAX_TIME_MIN = 3.5  # minutes (really for mobiles)

class Browser:
    """
    Class for wrapping selenium driver and controlling the remote browser in order to generate screenshots.
    Used by VisualTest class and should not be instantiated directly. 

    Args:
        driver: selenium webdriver with active session
        limits: Dictionary of values to change default limits for during creation fullpage images (not recommended)
            - MAX_IMAGE_PIXELS (int): Max fullpage image size. (default INT32 or 2^31)
            - MAX_TIME_MIN (float): Max time to create fullpage image.  Default is 3.5 minutes. Can be set to a max of 10 minutes. 
    Returns:
        Class instance
    """

    def __init__(self, driver, limits: dict = {}):

        if not driver:
            raise Exception('driver argument is required!')

        if not driver.session_id:
            raise Exception('driver argument does not have a session_id!')

        if not driver.capabilities:
            raise Exception('driver argument does not have capabilities!')

        # setup api
        self._userAgentScript = Api.getToolkit(script='userAgent')
        self._domCaptureScript = Api.getToolkit(script='domCapture')

        self._api = Api()
        log.info(f'Capabilities from driver: {driver.capabilities}')
        self._driver = driver
        self._userAgentInfo = self.getNavigatorUserAgentData(self._driver)
        self._deviceInfo = self._api.getDeviceInfo(self._userAgentInfo, driver.capabilities)
        log.info(f'Final device info: {self._deviceInfo}')

        log.info(f'limits: {limits}')
        if 'MAX_IMAGE_PIXELS' in limits:
            ImageTools.setMaxImagePixels(limits['MAX_IMAGE_PIXELS'])

        if 'MAX_TIME_MIN' in limits:
            self.MAX_TIME_MIN = limits['MAX_TIME_MIN']
        else:
            self._MAX_TIME_MIN = DEFAULT_MAX_TIME_MIN

        # default options
        self._scrollMethod = 'CSS_TRANSLATE'
        self._debugImages = False
        self._saveDOM = False

    @property
    def scrollMethod(self):
        return self._scrollMethod

    @scrollMethod.setter
    def scrollMethod(self, s):
        scroll_options = ['CSS_TRANSLATE', 'JS_SCROLL']
        if s in scroll_options:
            self._scrollMethod = s
        else:
            raise Exception(f'Invalid scrollMethod: "{s}". Options are {str(scroll_options)}')

    @property
    def capabilities(self):
        return self._driver.capabilities

    @property
    def debugImages(self):
        return self._debugImages

    @debugImages.setter
    def debugImages(self, debug):
        if type(debug) == bool:
            self._debugImages = debug
        else:
            raise Exception(f'Argument must be a boolean!')

    @property
    def saveDOM(self):
        return self._saveDOM

    @saveDOM.setter
    def saveDOM(self, save):
        if type(save) == bool:
            self._saveDOM = save
        else:
            raise Exception(f'Argument must be a boolean!')

    @property
    def MAX_TIME_MIN(self):
        return self._MAX_TIME_MIN

    @MAX_TIME_MIN.setter
    def MAX_TIME_MIN(self, minutes):
        if type(minutes) != int:
            raise Exception(f'MAX_TIME_MIN must be an integer')
        if minutes not in range(0, 11):
            raise Exception(f'MAX_TIME_MIN must be between 0 and 10 minutes')
        self._MAX_TIME_MIN = minutes

    def getNavigatorUserAgentData(self, driver):
        """ Using a custom predefined script, get info from browser's navigator.userAgent """
        agent = driver.execute_script(f'return {self._userAgentScript};')
        log.info(f'Browser info interpreted from navigator.userAgent: {agent}')

        # ensure is dictionary
        if type(agent) is not dict:
            log.info(f'navigator.userAgent was not a dictionary, the value was: {agent}')
            agent = {}

        return agent

    def captureDom(self, driver, path, type=""):
        """ Using a custom predefined script, capture the webpage's DOM element information """
        domString = driver.execute_script(f'return {self._domCaptureScript};')

        # add screenshot type and dump back to JSON string
        dom = json.loads(domString)
        dom['screenshotType'] = type
        domString = json.dumps(dom)
        # log.debug(f'Dom-capture: {dom}')

        if self._saveDOM: # save at same location and filename as screenshot
            with open(path.replace('.png','.json'), 'w') as outfile:
                json.dump(dom, outfile, indent=4)

        return dom

    def _findElement(self, cssSelector):
        return self._driver.find_element(By.CSS_SELECTOR, cssSelector)
    
    def _injectIgnoreElements(self, ignoreElements):
        script = 'window.sbvt = { ignoreElements: %s }' % json.dumps(ignoreElements)
        self._driver.execute_script(script)

    def _getPageDimensions(self):
        script = """
            return JSON.stringify({
                "document": {
                    "height": document.documentElement.clientHeight,
                    "width": document.documentElement.clientWidth
                },
                "body": {
                    "height": document.body.clientHeight,
                    "width": document.body.clientWidth
                },
                "windowInner": {
                    "height": window.innerHeight,
                    "width":  window.innerWidth
                },
                "fullpage": {
                    "height": Math.max(window.document.body.offsetHeight,window.document.body.scrollHeight, window.document.documentElement.offsetHeight, window.document.documentElement.scrollHeight),
                    "width": Math.max(window.document.body.offsetWidth,window.document.body.scrollWidth, window.document.documentElement.offsetWidth, window.document.documentElement.scrollWidth)
                },
                "devicePixelRatio": window.devicePixelRatio,
                "initialScroll": {
                    x: window.scrollX, 
                    y: window.scrollY
                }
            })
        """

        jsonDimensions = self._driver.execute_script(script)
        log.info(f'Webpage Dimensions: {jsonDimensions}')
        dimensions = json.loads(jsonDimensions)

        # for now, take the window.inner dimensions as viewport
        # there may be cases where we need the documentElement or body on older browsers
        self.viewportHeight = dimensions['windowInner']['height']
        self.viewportWidth = dimensions['windowInner']['width']
        self.fullpageHeight = dimensions['fullpage']['height']
        self.fullpageWidth = dimensions['fullpage']['width']
        self.devicePixelRatio = dimensions['devicePixelRatio']
        log.info(f'devicePixelRatio: {self.devicePixelRatio}')
        # validate the viewport from javascript matches 
        # what we actually get from a png
        file = os.path.join(self.tmpDir, f'size-test.png')
        self._driver.save_screenshot(file)
        testImageWidth, testImageHeight = ImageTools.getImageSize(file)
        log.info(f'Size Test: image dimensions: {testImageWidth}x{testImageHeight}')

        self._cropEachBottom = None
        self._cropEachTop = None

        expectedWidth = math.ceil(self.viewportWidth * self.devicePixelRatio)
        expectedHeight = math.ceil(self.viewportHeight * self.devicePixelRatio)

        # have to allow 1px difference for devicePixelRatio that has a fraction
        isExpectedWidth = expectedWidth - 1 <= testImageWidth <= expectedWidth + 1
        isExpectedHeight = expectedHeight - 1 <= testImageHeight <= expectedHeight + 1

        if (isExpectedWidth and isExpectedHeight):
            log.info(f'Size Test: image dimensions are exactly {self.devicePixelRatio}x the javascript viewport size')
        else:
            if (isExpectedWidth and not isExpectedHeight):
                log.info(f'Size Test: Image matches expected width but not height')
            else:
                log.info(f'Size Test: Neither height nor width matches between size-test image and javascript values')

            if self._deviceInfo['osName'] == 'android':
                # androids have extra white space at bottom of each screen capture
                self._cropEachBottom = testImageHeight - expectedHeight
                log.info(
                    f'Size Test: Android device has {self._cropEachBottom}px extra pixels to crop on each image at the bottom')
            elif self._deviceInfo['osName'] == 'ios':
                # iOSs have toolbars at top of each screen capture for iPads
                # but both on iPhones in portrait (mixed on landscape)
                # we cannot tell how much extra is top or bottom
                self._cropEachTop = testImageHeight - expectedHeight
                log.info(
                    f'Size Test: iOS device has {self._cropEachTop}px extra pixels to crop on each image (top and/or bottom)')
            else:
                raise Exception(f'Size Test: Unknown platform to handle when javascript values do not match image size')

    def _getInitialPageState(self):

        script = """
            return JSON.stringify({
                "scrollX": window.scrollX, 
                "scrollY": window.scrollY,
                "overflow": document.body.style.overflow,
                "transform": document.body.style.transform
            })
        """

        pageState = self._driver.execute_script(script)
        log.info(f'Webpage initial state: {pageState}')
        self.initialPageState = json.loads(pageState)

    def _getNumberOfPagesToScroll(self):

        # how many viewports do we have to scroll within the fullpage
        totalPages = math.ceil(self.fullpageHeight / self.viewportHeight)

        """ 
        LIMITING NUM OF PAGES SCROLLED
            The number of viewport heights (pages) we will scroll should
            be less than the MAX_IMAGE_PIXELS based on viewportWidth * viewportHeight
            Example: 
                vw = 1366 //viewport width
                vh = 683  //viewport height
                How many pages (viewport heights) can we scroll to be 
                less than or equal to MAX_IMAGE_PIXELS?

                pages = max / (vw * vh * ratio)
                pages = 5000 * 15000 / 1366 * 683 * 2 ~= 40
            But this won't matter as we'll test image file size as we go
        """
        log.debug(f'MAX_IMAGE_PIXELS: {ImageTools.getMaxImagePixels()}')
        maxPages = math.floor(
            ImageTools.getMaxImagePixels() / (self.viewportWidth * self.viewportHeight * self.devicePixelRatio))
        log.debug(f'maxPages based on MAX_IMAGE_PIXELS / (vw * vh * ratio): {maxPages}')

        if totalPages > maxPages:
            log.info('Total Pages was greater than max, so decreasing amount of possible screenshots')
            totalPages = maxPages

        return totalPages

    def _getScrollOffset(self):
        return self._driver.execute_script(
            'if (window.pageYOffset) return window.pageYOffset;else if (window.document.documentElement.scrollTop)'
            'return window.document.documentElement.scrollTop;else return window.document.body.scrollTop;')

    def _checkScrollingLimits(self, pageIndex, totalPages):

        # tuple for (hitLimit, reason)
        result = (False, None)

        # check time running so far
        elapsedTimeSecs = self.fullpageStopWatch.timeElapsed()
        elapsedTimeDisplay = f'{elapsedTimeSecs}s' if elapsedTimeSecs <= 120 else f'{round(elapsedTimeSecs / 60, 3)}m'
        log.debug(f'Fullpage elapsed time: {elapsedTimeDisplay}')
        # if we are on the last page or we didn't scroll, set done to true
        if pageIndex == totalPages - 1:
            log.info(f'STOPPING scroll and capture because on last of totalPages')
            result = (True, 'HIT_BOTTOM')
        elif self.approxDiskSize > DEFAULT_MAX_IMAGE_SIZE_MB * 1000 * 1000:
            log.info(f'STOPPING scroll and capture because image size is >= {DEFAULT_MAX_IMAGE_SIZE_MB}MB')
            result = (True, 'MAX_IMAGE_SIZE')
        elif elapsedTimeSecs / 60 > self._MAX_TIME_MIN:
            # if we are running out of time, set done to true
            log.info(f'STOPPING scroll and capture because exceeded MAX_TIMEOUT: {self._MAX_TIME_MIN} minutes')
            result = (True, 'MAX_TIME_LIMIT')
        elif self._scrollMethod == 'JS_SCROLL':
            # if we didn't scroll the full viewport (stopped early like when page is shorter than expected on mobiles)
            expectedScrollOffset = self.viewportHeight * pageIndex
            currentScrollOffset = math.ceil(self._getScrollOffset())  # ceil for mobiles that return decimal value
            if currentScrollOffset < expectedScrollOffset:
                log.info(f'STOPPING scroll and capture because we hit the bottom of the page sooner than expected')
                result = (True, 'HIT_BOTTOM')

        return result

    def _scrollPage(self, pageIndex):

        pixels = self.viewportHeight * pageIndex

        if self._scrollMethod == 'CSS_TRANSLATE':
            # transform page by -100vh for each page number
            # script = f'document.body.style.transform="translateY(-{100 * pageIndex}vh)"'
            script = f'document.body.style.transform="translateY(-{pixels}px)"'
            log.info(f'Scrolling with CSS_TRANSLATE: {script}')
            self._driver.execute_script(script)
            return True
        elif self._scrollMethod == 'JS_SCROLL':

            # to ensure we scrolled, check scroll offset before and after
            lastScrollOffset = self._getScrollOffset()

            # scroll by viewport height times page number
            script = f'window.scroll(0,{pixels})'
            self._driver.execute_script(script)
            log.info(f'Scrolling with JS_SCROLL: {script}')

            currentScrollOffset = self._getScrollOffset()
            log.info(f'Scroll offset before: {lastScrollOffset}, scroll offset after: {currentScrollOffset}')

            # if scroll offset is same as last scroll offset, 
            # we are waiting on the browser to finish the scroll task
            # or we have reached the bottom earlier than expected
            if lastScrollOffset == currentScrollOffset:
                log.info(
                    f'Last y offset same as current, waiting a few seconds to give browser time to scroll and testing offset again')
                time.sleep(4)  # wait a few seconds and test again
                currentScrollOffset = self._getScrollOffset()
                log.info(f'Scroll offset before: {lastScrollOffset}, scroll offset after: {currentScrollOffset}')
                if lastScrollOffset == currentScrollOffset:
                    log.info(
                        f'Last y offset same as current even after waiting a few seconds, done with screen captures')

            return lastScrollOffset < currentScrollOffset
        else:
            raise Exception(f'Invalid scroll method: {self._scrollMethod}')

    def _loadLazyContent(self, totalPages, waitTimeMs):
        log.info(f'Loading lazy content by scrolling entire page with wait time of: {waitTimeMs}ms')
        currentPage = 1
        while (currentPage <= totalPages):
            pixels = self.viewportHeight * currentPage
            script = f'window.scroll(0,{pixels})'
            self._driver.execute_script(script)
            log.info(f'Scrolling with JS_SCROLL: {script}')
            time.sleep(waitTimeMs / 1000)
            currentPage += 1
        
        self._driver.execute_script('window.scrollTo(0,0)')
        time.sleep(waitTimeMs / 1000)
        
    def _fullpageHeightChanged(self):

        changed = False
        # check if page has grown for lazy-loading or infinite scroll
        script = 'return Math.max(window.document.body.offsetHeight,window.document.body.scrollHeight, window.document.documentElement.offsetHeight, window.document.documentElement.scrollHeight)'
        newFullpageHeight = self._driver.execute_script(script)
        if newFullpageHeight != self.fullpageHeight:
            term = 'grew' if newFullpageHeight > self.fullpageHeight else 'shrank'
            log.info(f'Fullpage height {term}, was {self.fullpageHeight}, now is {newFullpageHeight}')
            self.fullpageHeight = newFullpageHeight
            changed = True

        return changed

    def _createTmpDir(self, path, screenshotType):
        current_time = time.strftime("%H-%M-%S", time.localtime()) # removed the ":" because throw error with windows
        self.tmpDir = os.path.join(path, f'.temp-images-{screenshotType}-{current_time}')
        os.makedirs(self.tmpDir)
        log.info(f'Made tmp images directory for {screenshotType} screenshot: {self.tmpDir}')

    def _deleteTmpDir(self):
        # there can only be one screenshot happening at a time,
        # hence there can only be one tmpDir referenced on self
        try:
            shutil.rmtree(self.tmpDir)
            log.info(f'Deleted tmp images directory: {self.tmpDir}')
            self.tmpDir = None
        except OSError as e:
            log.warning(f'Error deleting tmp directory: {e.filename} - {e.strerror}.')

    def takeFullpageScreenshot(self, path: str, lazyload=None):
        """
        Will take a fullpage screenshot and place the image at the path provided. \n
        Note this places a temporary folder at the current directory with the name sbTemp-{time}
        Args:
            path (str): the directory for where to save the image
            lazyload (int): if set, will scroll the page to load any content first and wait the number of milliseconds provided between each scroll
        """

        if self._deviceInfo['osName'] == 'ios':
            raise Exception('iOS devices do no currently support fullpage screenshots.')

        log.info(f'Taking full page screenshot at URL: {self._driver.current_url}')
        if '.png' not in path:
            raise Exception('Fullpage Screenshot path must end in a .png')

        # limit how long we let a screenshot run
        self.fullpageStopWatch = StopWatch()
        self.fullpageStopWatch.start()

        # create tmp directory for storing images that will be stitched together
        self._createTmpDir(os.path.dirname(path), 'fullpage')

        # get initial page state for returning to later (must do before hiding scrollbar)
        self._getInitialPageState()

        # hide scroll bar for accurate dimensions
        hideScrollBarResult = self._driver.execute_script('return document.body.style.overflow="hidden";')
        log.info(f'PREP: Hide scrollbar result: {hideScrollBarResult}')

        # update the dimensions of the browser window and webpage
        self._getPageDimensions()

        # how many viewports fit into the fullpage 
        totalPages = self._getNumberOfPagesToScroll()
        log.info(f'Total pages to scroll: {totalPages}')

        reasonStopped = None

        # handle single page as special case
        if totalPages == 1:
            # take the selenium screenshot as final fullpage
            log.info(f'Taking single screenshot for single page')

            pageStopWatch = StopWatch()
            pageStopWatch.start()
            totalPageTime = 0

            file = os.path.join(self.tmpDir, f'0.png')
            self._driver.save_screenshot(file)

            if self._cropEachBottom:
                file = ImageTools.cropBottom(file, self._cropEachBottom)

            if self._cropEachTop:
                file = ImageTools.cropTop(file, self._cropEachTop)

            # copy file to save path
            shutil.copy(file, path)
            reasonStopped = 'IS_SINGLE_PAGE'

            # capture dom AFTER creating screenshot but BEFORE displaying scrollbar again (else get vertical offset on dom elements to image)
            self.dom = self.captureDom(self._driver, path, 'fullpage')

            log.info(f'Setting document.body.style.overflow back to initial state: {self.initialPageState["overflow"]}')
            self._driver.execute_script(f'document.body.style.overflow="{self.initialPageState["overflow"]}"')

            pageTime = pageStopWatch.stop()
            averagePageTime = round(pageTime, 2)

        else:

            # scroll browser back to initial position
            log.info(f'PREP: Scrolling to top of page')
            self._driver.execute_script('window.scrollTo(0,0)')

            # handle lazy-loaded content if setting provided
            if lazyload != None:
                self._loadLazyContent(totalPages, lazyload)

            # to hide bottom fixed elements, this is a trick that works on most modern browsers
            log.info(f'PREP: Hiding bottom fixed elements: document.body.style.transform="translateY(0)"')
            self._driver.execute_script(f'document.body.style.transform="translateY(0)"')
            time.sleep(0.5) #some browsers need a little time to apply (Safari)

            done = False
            pageIndex = 0
            screenshots = []
            self.approxDiskSize = 0

            pageStopWatch = StopWatch()
            pageStopWatch.start()
            totalPageTime = 0

            # main loop for scroll and capture
            while not done:
                log.info(f'-- PAGE {pageIndex} --')
                scrolled = True

                # don't scroll for first pageIndex
                if pageIndex > 0:

                    # scroll and check scrolled correctly
                    scrolled = self._scrollPage(pageIndex)

                    # check if the page height changed
                    if self._fullpageHeightChanged():
                        newTotalPages = self._getNumberOfPagesToScroll()
                        if newTotalPages > totalPages:
                            totalPages = newTotalPages
                            log.info(f'Total pages is now {totalPages}')
                            # if grew, scroll again to same position to ensure 
                            # handles infinite-scroll or lazy loaded content
                            self._scrollPage(pageIndex)

                # check if we should stop scrolling due to a limit
                hitLimit, reasonStopped = self._checkScrollingLimits(pageIndex, totalPages)

                # take the selenium screenshot
                file = os.path.join(self.tmpDir, f'{pageIndex}.png')
                self._driver.save_screenshot(file)

                if self._cropEachBottom:
                    file = ImageTools.cropBottom(file, self._cropEachBottom)

                if self._cropEachTop:
                    file = ImageTools.cropTop(file, self._cropEachTop)

                # crop image as necessary
                if self._scrollMethod == 'CSS_TRANSLATE':

                    """
                    When using translate, the last page will be shifted up past the true
                    bottom of the page. We need to crop off the extra "white" space that 
                    will be included in this last screenshot.

                    To calculate, get the remainder of "viewport" modulo "fullpage", which
                    is number of pixels we want to keep from the top. Subtract that from the 
                    viewport height to get the number of pixels to crop off at the bottom.

                    Multiply by devicePixelRatio to get the actual pixels for image crop.
                    """

                    cropHeight = self.viewportHeight - (self.fullpageHeight % self.viewportHeight)
                    numPixels = cropHeight * self.devicePixelRatio

                    if pageIndex == totalPages - 1 and numPixels > 0:
                        log.info(f'Cropping bottom of last image: {numPixels}px')
                        file = ImageTools.cropBottom(file, numPixels)  # will reference cropped file

                elif self._scrollMethod == 'JS_SCROLL':

                    """
                    When using window.scrollTo(), the last page will not scroll a full
                    viewport and our last image will have content at the top that duplicates
                    content from previous screenshot. So, we need to crop the top of the image
                    to create a seamless stitch.

                    To calculate, subtract the scrolled offset from total viewports scrolled
                    and multiply by devicePixelRatio to get the actual pixels for image crop.
                    """
                    cropHeight = pageIndex * self.viewportHeight - self._getScrollOffset()
                    numPixels = cropHeight * self.devicePixelRatio
                    if hitLimit and reasonStopped == 'HIT_BOTTOM' and numPixels > 0:
                        log.info(f'Cropping top of last image: {numPixels}px')
                        file = ImageTools.cropTop(file, numPixels)  # will reference cropped file

                screenshots.append(file)
                self.approxDiskSize += os.path.getsize(file)

                # we are done if we didn't actually scroll or hit a scrolling limit
                done = not scrolled or hitLimit
                pageTime = pageStopWatch.stop()
                totalPageTime += pageTime
                log.debug(f'Scroll and capture page time: {pageTime}s')

                # increment pageIndex
                pageIndex += 1

            averagePageTime = round(totalPageTime / pageIndex, 2)

            if self._scrollMethod == 'CSS_TRANSLATE':
                # put back to the top while capturing don
                self._driver.execute_script(f'document.body.style.transform="translateY(0)"')

            elif self._scrollMethod == 'JS_SCROLL':
                #scroll back to the top
                self._driver.execute_script('window.scrollTo(0,0)')
                time.sleep(0.75) # wait a half sec to allow dom to settle before capturing

            # capture dom AFTER creating screenshot but BEFORE setting back to initial states
            self.dom = self.captureDom(self._driver, path, 'fullpage')

            # Setting document.body.style.transform back
            log.info(f'Setting document.body.style.transform back to initial state: {self.initialPageState["transform"]}')
            self._driver.execute_script(f'document.body.style.transform="{self.initialPageState["transform"]}"')
            
            # Setting scroll position back
            log.info(f'Scrolling back to initial scroll offset ({self.initialPageState["scrollX"]},{self.initialPageState["scrollY"]})')
            self._driver.execute_script(
                f'window.scrollTo({self.initialPageState["scrollX"]},{self.initialPageState["scrollY"]})')
            
            # Showing scrollbar again by setting overflow back
            log.info(f'Setting document.body.style.overflow back to initial state: {self.initialPageState["overflow"]}')
            self._driver.execute_script(f'document.body.style.overflow="{self.initialPageState["overflow"]}"')

            # TODO: technically we could return control back to user here??

            # build the fullpage image from individual screenshots
            log.info(f'Stitching screenshots for final fullpage image')
            ImageTools.stitchImages(screenshots, path)
        

        # validate final fullpage image dimensions
        imageWidth, imageHeight = ImageTools.getImageSize(path)

        expectedImageWidth = self.fullpageWidth * self.devicePixelRatio
        expectedImageHeight = self.fullpageHeight * self.devicePixelRatio

        totalFullpageTime = self.fullpageStopWatch.stop()
        log.info(f'Total fullpage time duration: {totalFullpageTime} seconds')
        result = {
            'imagePath': path,
            'imageSize': {
                'width': imageWidth,
                'height': imageHeight
            },
            'expectedSize': {
                'width': expectedImageWidth,
                'height': expectedImageHeight
            },
            'devicePixelRatio': self.devicePixelRatio,
            'reasonStopped': reasonStopped,
            'duration': f'{totalFullpageTime} seconds',
            'averagePageTime': f'{averagePageTime} seconds',
            'url': self._driver.current_url
        }

        log.info(f'Result: {result}')
        result['dom'] = self.dom #add dom after logging result

        # delete the temp screenshot images used to build fullpage
        if not self._debugImages:
            self._deleteTmpDir()

        return result

    def takeElementScreenshot(self, element, path):
        """
        Will take an element screenshot and place the image at the path provided. \n
        Args:
            element (WebElement): The reference to the Selenium WebElement to capture a screenshot of
            path (str): the directory for where to save the image
        """
        # measure how long it takes
        self.watch = StopWatch()
        self.watch.start()

        # create tmp directory for storing images that will be stitched together
        self._createTmpDir(os.path.dirname(path), 'element')

        # update the dimensions of the browser window and webpage
        self._getPageDimensions()

        # selenium.webdriver.firefox.webelement.FirefoxWebElement
        log.debug(f'type of element is {type(element)}')
        log.info(f'Taking element screenshot of element')
        element.screenshot(path)

        # capture dom AFTER creating screenshot
        self.dom = self.captureDom(self._driver, path, 'element')

        # validate final fullpage image dimensions
        imageWidth, imageHeight = ImageTools.getImageSize(path)

        totalTime = self.watch.stop()
        result = {
            'imagePath': path,
            'imageSize': {
                'width': imageWidth,
                'height': imageHeight
            },
            'duration': f'{totalTime} seconds',
            'url': self._driver.current_url
        }

        log.info(f'Result: {result}')
        result['dom'] = self.dom #add dom after logging result

        if not self._debugImages:
            self._deleteTmpDir()

        return result

    def takeViewportScreenshot(self, path):
        """
        Will take a screenshot of the browser viewport and place the image at the path provided. \n
        Args:
            path (str): the directory for where to save the image
        """
        log.info(f'Taking screenshot of viewport')

        # measure how long it takes
        self.watch = StopWatch()
        self.watch.start()

        # create tmp directory for storing images that will be stitched together
        self._createTmpDir(os.path.dirname(path), 'viewport')

        # get initial page state for returning to later (must do before hiding scrollbar)
        self._getInitialPageState()

        # hide scroll bar for accurate dimensions
        hideScrollBarResult = self._driver.execute_script('return document.body.style.overflow="hidden";')
        log.info(f'PREP: Hide scrollbar result: {hideScrollBarResult}')

        # update the dimensions of the browser window and webpage
        self._getPageDimensions()

        file = os.path.join(self.tmpDir, f'viewport.png')
        self._driver.save_screenshot(file)

        if self._cropEachBottom:
            file = ImageTools.cropBottom(file, self._cropEachBottom)

        if self._cropEachTop:
            file = ImageTools.cropTop(file, self._cropEachTop)

        # copy file to save path
        shutil.copy(file, path)

        # capture dom AFTER creating screenshot but BEFORE displaying scrollbar again (else get vertical offset on dom elements to image)
        self.dom = self.captureDom(self._driver, path, 'viewport')

        log.info(f'Setting document.body.style.overflow back to initial state: {self.initialPageState["overflow"]}')
        self._driver.execute_script(f'document.body.style.overflow="{self.initialPageState["overflow"]}"')

        # validate final fullpage image dimensions
        imageWidth, imageHeight = ImageTools.getImageSize(path)

        expectedImageWidth = self.viewportWidth * self.devicePixelRatio
        expectedImageHeight = self.viewportHeight * self.devicePixelRatio

        totalTime = self.watch.stop()
        log.info(f'Total viewport capture time duration: {totalTime} seconds')
        result = {
            'imagePath': path,
            'imageSize': {
                'width': imageWidth,
                'height': imageHeight
            },
            'expectedSize': {
                'width': expectedImageWidth,
                'height': expectedImageHeight
            },
            'devicePixelRatio': self.devicePixelRatio,
            'duration': f'{totalTime} seconds',
            'url': self._driver.current_url
        }

        log.info(f'Result: {result}')
        result['dom'] = self.dom #add dom after logging result

        if not self._debugImages:
            self._deleteTmpDir()

        return result
