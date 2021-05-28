/* jshint esversion:6 */

/**
 * slider class
 */
class VanillaSlider {

    /**
     * @param {any} containerId element or id of element which shall be the container for the slider;
     * @param {{images: Array<any>, transitionTime: number, transitionDirectionX: string, transitionDirectionY: string, transitionZoom: string, swipe: boolean, auto: boolean, autoTime: number}} options options object for slider:
     * options.images: array of images, either strings (URLs) or objects with imageUrl, linkUrl, linkNewTab, textTitle, textBody, textPosition
     * options.transitionTime: time in ms until transition is finished;
     * options.transitionDirectionX: x direction for fading out element to move - 'left', 'right', or 'random'
     * options.transitionDirectionY: y direction for fading out element to move - 'up', 'down', or 'random'
     * options.transitionZoom: direction for zooming the fading out element - 'in', 'out', or 'random'
     * options.swipe: whether to allow swipe support
     * options.auto: whether to automatically move slides
     * options.autoTime: time in ms for slides to automatically move
     * options.autoPauseOnHover: whether to pause auto on mouse hover
     */
    constructor(containerId, options = {}) {

        this.containerId = containerId;
        this.images = options.images;
        this.transitionTime = options.transitionTime;
        this.transitionDirectionX = options.transitionDirectionX;
        this.transitionDirectionY = options.transitionDirectionY;
        this.transitionZoom = options.transitionZoom;
        this.swipe = options.swipe;
        this.auto = options.auto;
        this.autoTime = options.autoTime;
        this.autoPauseOnHover = options.autoPauseOnHover;
        this.webp = options.webp;

        this.currentIndex = 0; // index of currently shown image 
        this.sliderLock = false; // slider is locked and can't transition
        this.imageElements = []; // image elements
        this.hover = false; // true on mouse in, false on mouse out
        this.autoPaused = false;
        this.touch = 'ontouchstart' in document.documentElement; // true if browser supports touch

        // adjusting values
        this.transitionTime = this.transitionTime ? this.transitionTime : 250;
        this.swipe = typeof this.swipe === 'boolean' ? this.swipe : true;
        this.auto = typeof this.auto === 'boolean' ? this.auto : false;
        this.autoTime = typeof this.autoTime === 'number' ? this.autoTime : 10000;
        this.autoPauseOnHover = typeof this.autoPauseOnHover === 'boolean' ? this.autoPauseOnHover : true;
        this.webp = typeof this.webp === 'boolean' ? this.webp : false;
        if (this.webp) {
            var ff = window.navigator.userAgent.match(/Firefox\/([0-9]+)\./);
            var ffVer = ff ? parseInt(ff[1]) : 0;
            var ffSupport = ffVer > 64;

            var ua = window.navigator.userAgent;
            var edge = ua.indexOf('Edge/');
            var ieSupport = parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10) > 17;

            var webpTest;
            var elem = document.createElement('canvas');
            if (!!(elem.getContext && elem.getContext('2d'))) {
                // was able or not to get WebP representation
                webpTest = elem.toDataURL('image/webp').indexOf('data:image/webp') == 0;
            }
            this.webp = (webpTest || ffSupport || ieSupport);
        }

        if (!Array.isArray(this.images)) {
            this.images = null;
        }

        if (typeof this.containerId !== 'string') {
            if (this.containerId.id) {
                this.containerId = this.containerId.id;
            }
        }

        if (!document.getElementById(this.containerId)) {
            throw ("Slider error: containerId must be a valid element or id");
        }

        // place images in container
        var imageElement;
        var imageAnchor;
        var imagesIndex = 0;
        this.container = document.getElementById(this.containerId);
        if (!this.images) {
            this.images = [];
            var containerChildren = this.container.children;

            [].forEach.call(containerChildren, (containerChild) => {
                imageAnchor = null;
                if (containerChild.tagName === 'A') {
                    imageAnchor = containerChild;
                    containerChild = containerChild.firstElementChild;
                }
                if (containerChild.tagName === 'IMG') {
                    this.images[imagesIndex] = {};
                    this.images[imagesIndex].imageUrl = containerChild.src;
                    if (imageAnchor) {
                        this.images[imagesIndex].linkUrl = imageAnchor.href;
                        this.images[imagesIndex].linkNewTab = imageAnchor.target === '_blank';
                    }
                    if (containerChild.hasAttribute('text-title')) {
                        this.images[imagesIndex].textTitle = containerChild.getAttribute('text-title');
                    }
                    if (containerChild.hasAttribute('text-body')) {
                        this.images[imagesIndex].textBody = containerChild.getAttribute('text-body');
                    }
                    if (containerChild.hasAttribute('text-position')) {
                        this.images[imagesIndex].textPosition = containerChild.getAttribute('text-position');
                    }
                    if (containerChild.hasAttribute('webp-url')) {
                        this.images[imagesIndex].webpUrl = containerChild.getAttribute('webp-url');
                    }
                    if (containerChild.hasAttribute('alt')) {
                        this.images[imagesIndex].alt = containerChild.getAttribute('alt');
                    }
                    if (containerChild.hasAttribute('title')) {
                        this.images[imagesIndex].title = containerChild.getAttribute('title');
                    }
                    imagesIndex++;
                } else {
                    console.log('Slider error: invalid container child tag name: ' + containerChild.tagName);
                }
            });
        }

        this.container.innerHTML = '';

        this.images.forEach((image, index) => {
            if (typeof image === 'string') {
                image = {
                    imageUrl: image,
                    linkUrl: null,
                    linkNewTab: null
                };
            }
            imageElement = document.createElement('IMG');
            imageElement.id = this.containerId + "-slide-" + index;
            if (this.webp && image.webpUrl) {
                imageElement.src = image.webpUrl;
            } else {
                imageElement.src = image.imageUrl;
            }
            imageElement.classList.add('vanilla-slider-image');
            //imageElement.style.margin = 'auto';
            imageElement.style.maxWidth = '100%';
            imageElement.style.position = 'absolute';
            imageElement.style.top = 0;
            imageElement.style.left = 0;
            if(image.alt) {
                imageElement.alt = image.alt;
            }
            if(image.title) {
                imageElement.title = image.title;
            }

            if (index > 0) {
                imageElement.style.visibility = 'hidden';
                imageElement.style.zIndex = 0;
            } else {
                imageElement.style.zIndex = 2;
            }
            this.container.appendChild(imageElement);
            if (index === this.images.length - 1) {
                imageElement.onload = () => {
                    
                    this.container.style.width = Math.min(imageElement.naturalWidth, document.body.clientWidth) + 'px';
                    this.container.style.height = Math.min(imageElement.naturalHeight, document.body.clientHeight) + 'px';
                    this.container.style.width = imageElement.clientWidth + 'px';
                    this.container.style.height = imageElement.clientHeight + 'px';
                };
            }
            
            this.imageElements[index] = imageElement;
        });
        if (this.images.length < 1) {
            throw ('Slider error: no images found for slides.');
        }

        const isIE = () => {
            return navigator.userAgent.indexOf("MSIE ") > -1 || navigator.userAgent.indexOf("Trident/") > -1;
        };

        // // style container
        // this.container.classList.add('vanilla-slider-container');
        // if(isIE()) {
        //     this.container.style.alignItems = 'flex-end';
        // }
        
        /**
         * fades the target out
         * @param {element||string} fadeOutTarget element to fade out, or its id
         * @param {function} callback function executed when fade is finished
         * @param {{waitTime: any, fadeTime: number, direction: string, zoom: string}} options options object for fade:
         * options.waitTime: wait before executing - true for 2 sec, false for 0 sec, num for other (ms);
         * options.fadeTime: time for the fadeIn/fadeOut effects, defaults to 250;
         * options.direction: direction for the fading out element to fly away if position:aboslute (left, right, up, down) - null to stay still;
         * options.zoom: direction for the fading element to zoom if position:absolute (in, out) - null to stay same size
         */
        this.slideFadeOut = (fadeOutTarget, callback = () => {}, options = []) => {

            // check cb
            if (typeof callback !== 'function') {
                callback = () => {};
            }

            // check target
            if (typeof fadeOutTarget === 'string') {
                fadeOutTarget = document.getElementById(fadeOutTarget);
            }

            // static values
            const defaultWaitTime = 2000;
            const defaultFadeTime = 500;
            const intervalTime = 20;
            const xDirections = ['left', 'right', 'random'];
            const yDirections = ['up', 'down', 'random'];
            const zooms = ['in', 'out', 'random'];

            // default options
            options.waitTime = options.waitTime ? options.waitTime : false;
            options.fadeTime = options.fadeTime ? options.fadeTime : defaultFadeTime;
            options.directionX = options.directionX ? options.directionX : null;
            options.directionY = options.directionY ? options.directionY : null;
            // options.zoom = options.zoom ? options.zoom : null;
            options.zoom = null;


            var isVisible = (element) => {
                return element.style.visibility !== "hidden";
            };
            var makeInvisible = (element) => {
                element.style.visibility = "hidden";
            };

            if (fadeOutTarget) {
                if (isVisible(fadeOutTarget)) {
                    // set zoom/direction
                    if (options.directionX) {
                        options.directionX = xDirections.includes(options.directionX) ? options.directionX : null;
                        if (options.directionX === 'random') {
                            options.directionX = ['right', 'left', null][Math.floor(Math.random() * 3)];
                        }
                        var xDirectionInterval;
                        switch (options.directionX) {
                            case 'right':
                                xDirectionInterval = 1;
                                break;
                            case 'left':
                                xDirectionInterval = -1;
                                break;
                        }
                    }
                    if (options.directionY) {
                        options.directionY = yDirections.includes(options.directionY) ? options.directionY : null;
                        if (options.directionY === 'random') {
                            options.directionY = ['up', 'down', null][Math.floor(Math.random() * 3)];
                        }
                        var yDirectionInterval;
                        switch (options.directionY) {
                            case 'up':
                                yDirectionInterval = -1;
                                break;
                            case 'down':
                                yDirectionInterval = 1;
                                break;
                        }
                    }
                    if (options.zoom) {
                        options.zoom = zooms.includes(options.zoom) ? options.zoom : null;
                        if (options.zoom === 'random') {
                            options.zoom = ['in', 'out', null][Math.floor(Math.random() * 3)];
                        }
                        var zoomInterval;
                        switch (options.zoom) {
                            case 'in':
                                zoomInterval = 0.005;
                                break;
                            case 'out':
                                zoomInterval = -0.005;
                                break;
                        }
                    }
                    if (options.waitTime) {
                        options.waitTime = options.waitTime === true ? defaultWaitTime : options.waitTime;
                        options.waitTime = typeof options.waitTime === 'number' ? options.waitTime : defaultWaitTime;
                        setTimeout(() => {
                            options.waitTime = false;
                            this.slideFadeOut(fadeOutTarget, callback, options);
                        }, options.waitTime);
                    } else {
                        options.fadeTime = typeof options.fadeTime === 'number' ? options.fadeTime : defaultFadeTime;
                        var opacityInterval = intervalTime / options.fadeTime;
                        fadeOutTarget.style.opacity = 1;
                        var fadeOutEffect = setInterval(() => {
                            if (fadeOutTarget.style.opacity > 0) {
                                // fade out a little bit
                                fadeOutTarget.style.opacity -= opacityInterval;
                                // move a little bit in directions
                                if (options.directionX) {
                                    fadeOutTarget.style.left = (parseFloat(fadeOutTarget.style.left.replace('px', '')) + xDirectionInterval) + 'px';
                                }
                                if (options.directionY) {
                                    fadeOutTarget.style.top = (parseFloat(fadeOutTarget.style.top.replace('px', '')) + yDirectionInterval) + 'px';
                                }
                                // zoom a little bit
                                if (options.zoom) {
                                    if (!fadeOutTarget.style.transform) {
                                        fadeOutTarget.style.transform = 'scale(1)';
                                    }
                                    fadeOutTarget.style.transform = 'scale(' + (parseFloat(fadeOutTarget.style.transform.replace('scale(', '').replace(')', '')) + zoomInterval) + ')';
                                }
                            } else {
                                clearInterval(fadeOutEffect);
                                makeInvisible(fadeOutTarget);
                                // console.log('top: ' + fadeOutTarget.style.top);
                                // console.log('left: ' + fadeOutTarget.style.left);
                                fadeOutTarget.style.top = 0;
                                fadeOutTarget.style.left = 0;
                                fadeOutTarget.style.transform = 'scale(1)';
                                callback();
                            }
                        }, intervalTime);
                    }
                } else {
                    callback();
                    // setTimeout(callback, options.fadeTime);
                }
            } else {
                console.log('fadeOut error: no such element exists.');
            }
        };

        /**
         * get the index of the next slide
         */
        this.getNextIndex = () => {
            return (this.currentIndex + 1) % this.imageElements.length;
        };

        /**
         * get the index of the previous slide
         */
        this.getPrevIndex = () => {
            return this.currentIndex < 1 ? this.imageElements.length - 1 : this.currentIndex - 1;
        };

        /**
         * go to the next slide, then execute the callback
         */
        this.nextSlide = (callback = null) => {
            this.goToSlide(this.getNextIndex(), callback);
        };

        /**
         * go to the previous slide, then execute the callback
         */
        this.prevSlide = (callback = null) => {
            this.goToSlide(this.getPrevIndex(), callback);
        };

        /**
         * go to the slide at index (if possible), then execute the callback
         */
        this.goToSlide = (newIndex, callback = null) => {
            if (typeof newIndex !== 'number' || newIndex < 0 || newIndex + 1 > this.imageElements.length) {
                console.log('Slider error: invalid index in goToSlide: ' + newIndex);
                if (typeof callback === 'function') {
                    callback();
                }
            } else if (newIndex === this.currentIndex) {
                console.log('Slider error: current index in goToSlide: ' + newIndex);
                if (typeof callback === 'function') {
                    callback();
                }
            } else if (!this.sliderLock) {
                this.pauseAuto();
                var finishSlide = () => {
                    this.currentIndex = newIndex;
                    this.sliderLock = false;
                    if (typeof callback === 'function') {
                        callback();
                    }
                    if (!this.autoPauseOnHover || !this.hover || this.touch) {
                        this.resumeAuto();
                    }
                };
                this.sliderLock = true;
                this.transitionSlide(newIndex, finishSlide);
            } else {
                console.log('Slider error: slider is locked.');
            }
        };

        /**
         * start automatic slide movement
         */
        this.startAuto = () => {
            this.auto = true;
            this.autoInterval = setInterval(this.nextSlide, this.autoTime);
        };

        /**
         * pause automatic slide movement until slides move
         */
        this.pauseAuto = () => {
            if (this.auto && !this.autoPaused) {
                clearInterval(this.autoInterval);
                this.autoPaused = true;
            }
        };

        /**
         * pause automatic slide movement until slides move
         */
        this.resumeAuto = () => {
            if (this.auto && this.autoPaused) {
                this.autoInterval = setInterval(this.nextSlide, this.autoTime);
                this.autoPaused = false;
            }
        };

        /**
         * stop automatic slide movement
         */
        this.stopAuto = () => {
            clearInterval(this.autoInterval);
            this.auto = false;
        };

        /**
         * clear the link div for the slide, and if the next slide has a link, create the link div
         */
        this.setSlideLink = (index) => {
            if (this.linkOverlay) {
                this.container.removeChild(this.linkOverlay);
                this.linkOverlay = null;
            }
            if (this.images[index].linkUrl) {
                this.linkOverlay = document.createElement('DIV');
                this.linkOverlay.id = this.containerId + '-link-overlay';
                this.linkOverlay.classList.add('vanilla-slider-link-overlay');
                this.linkOverlay.style.zIndex = 5;
                this.linkOverlay.style.position = 'absolute';
                this.linkOverlay.style.top = 0;
                this.linkOverlay.style.left = 0;
                this.linkOverlay.style.width = '100%';
                this.linkOverlay.style.height = '100%';
                this.linkOverlay.style.cursor = 'pointer';
                if (this.images[index].linkNewTab) {
                    this.linkOverlay.addEventListener('click', () => {
                        window.open(this.images[index].linkUrl, '_blank');
                    });
                } else {
                    this.linkOverlay.addEventListener('click', () => {
                        window.location.href = this.images[index].linkUrl;
                    });
                }
                this.container.appendChild(this.linkOverlay);
            }
        };

        /**
         * transition from one slide to another
         */
        this.transitionSlide = (newIndex, callback) => {
            this.imageElements[newIndex].style.zIndex = 1;
            this.imageElements[newIndex].style.opacity = 1;
            this.imageElements[newIndex].style.visibility = 'visible';
            this.slideFadeOut(this.imageElements[this.currentIndex], () => {
                this.imageElements[this.currentIndex].style.zIndex = 0;
                this.imageElements[newIndex].style.zIndex = 2;
                callback();
            }, {
                fadeTime: this.transitionTime,
                directionX: this.transitionDirectionX,
                directionY: this.transitionDirectionY,
                zoom: this.transitionZoom
            });
        };


        // set swipe listener
        if (this.swipe) {

            this.swiper = {};

            this.swiper.xDown = null;
            this.swiper.yDown = null;

            this.container.addEventListener('touchstart', (evt) => {
                this.swiper.xDown = evt.touches[0].clientX;
                this.swiper.yDown = evt.touches[0].clientY;
            }, false);

            var handleTouchMove = (evt) => {
                if (!this.swiper.xDown || !this.swiper.yDown) {
                    return;
                }

                var xUp = evt.touches[0].clientX;
                var yUp = evt.touches[0].clientY;

                this.swiper.xDiff = this.swiper.xDown - xUp;
                this.swiper.yDiff = this.swiper.yDown - yUp;

                if (Math.abs(this.swiper.xDiff) > Math.abs(this.swiper.yDiff)) { // Most significant.
                    var transition = {};
                    if (this.swiper.xDiff > 0) {
                        transition = {
                            x: this.transitionDirectionX,
                            y: this.transitionDirectionY,
                            z: this.transitionZoom
                        };
                        this.transitionDirectionX = 'left';
                        this.transitionDirectionY = false;
                        this.transitionZoom = false;
                        this.nextSlide(() => {
                            this.transitionDirectionX = transition.x;
                            this.transitionDirectionY = transition.y;
                            this.transitionZoom = transition.z;
                        });
                    } else {
                        transition = {
                            x: this.transitionDirectionX,
                            y: this.transitionDirectionY,
                            z: this.transitionZoom
                        };
                        this.transitionDirectionX = 'right';
                        this.transitionDirectionY = false;
                        this.transitionZoom = false;
                        this.prevSlide(() => {
                            this.transitionDirectionX = transition.x;
                            this.transitionDirectionY = transition.y;
                            this.transitionZoom = transition.z;
                        });
                    }
                }

                // Reset values.
                this.swiper.xDown = null;
                this.swiper.yDown = null;
            };

            this.container.addEventListener('touchmove', (evt) => {
                handleTouchMove(evt);
            }, false);
        }

        // start automatic slide movement
        if (this.auto) {
            this.startAuto();

            // place mouse listeners for auto pause/resume
            if (this.autoPauseOnHover) {
                this.container.addEventListener('mouseenter', () => {
                    this.pauseAuto();
                });
                this.container.addEventListener('mouseleave', () => {
                    this.resumeAuto();
                });
            }
        }

        if(!this.touch) {
            // set listeners for hover property
            this.container.addEventListener('mouseenter', () => {
                this.hover = true;
            });
            this.container.addEventListener('mouseleave', () => {
                this.hover = false;
            });
        }
    }
}

/**
 * Returns a VanillaSlider created from containerId and options
 * @param {string|Node} containerId element or id of element to be the slider container
 * @param {object} options slider options object for slider configuration
 */
function createSlider(containerId, options) {
    return new VanillaSlider(containerId, options);
}

/**
 * includes polyfill
 */
if (!Array.prototype.includes) {
    Object.defineProperty(Array.prototype, "includes", {
        enumerable: false,
        value: function (obj) {
            var newArr = this.filter(function (el) {
                return el == obj;
            });
            return newArr.length > 0;
        }
    });
}
