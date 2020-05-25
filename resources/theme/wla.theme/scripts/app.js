"use strict";

requirejs(['require', '/scripts/svg4everybody.js', '/scripts/flickity.pkgd.js', '/scripts/slider.js', '/scripts/paneleditor.js', '/scripts/x-ray.js', '/scripts/Sortable.min.js', '/scripts/choices.min.js', '/scripts/fontfaceobserver.js', '/scripts/respimage.js', '/scripts/ls.parent-fit.js', '/scripts/lazysizes-umd.js', '/scripts/a25.js', '/scripts/a25.navbar.js'], function (require, svg4everybody, Flickity, slider, panelEditor, xrays, SortableJS, Choices) {
  'use strict'; // Trigger font face observer protection

  var fontPrimary = new FontFaceObserver('Open Sans', {
    weight: 400
  });
  fontPrimary.load(null, 3000).then(function () {
    document.documentElement.className += " font__primary--loaded";
  });
  Promise.all([fontPrimary.load(null, 3000)]).then(function () {
    document.documentElement.className += " fonts--loaded";
  });

  if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
    document.documentElement.className += " u-device--ios";
  }

  ; // SVG Sprite polyfill

  svg4everybody(); // Panel page and widget editor

  panelEditor.init(); // Choices select

  var choicesSelector = document.querySelector('.js-choices-selector');

  if (choicesSelector !== null) {
    var choices = new Choices(choicesSelector, {
      itemSelectText: 'auswählen'
    });
  } // Panel Editor Sortable


  var sortableSection = document.querySelector('.js-sortable');

  if (sortableSection !== null) {
    var sortable = SortableJS.create(sortableSection, {
      handle: ".js-sortable-handle",
      ghostClass: "c-sortable__ghost",
      // Class name for the drop placeholder
      chosenClass: "c-sortable__chosen",
      // Class name for the chosen item
      dragClass: "c-sortable__drag",
      // Class name for the dragging item
      dataIdAttr: 'data-id',
      onSort: function onSort(event) {
        // same properties as onEnd
        var items = event.to.children,
            result = [];

        for (var i = 0; i < items.length; i++) {
          result.push(items[i].getAttribute('data-id'));
        }
        /* Do ajax call here */


        var sourceUrl = sortableSection.dataset.storage,
            targetEl = sortableSection,
            formData = new FormData();
        formData.append("order", JSON.stringify(result));
        var request = new XMLHttpRequest();
        request.open('POST', sourceUrl, true);

        request.onload = function (e) {
          if (request.status >= 200 && request.status < 400) {
            // Success!
            var response = request.responseText,
                responseData = JSON.stringify(response),
                returnData = JSON.parse(response);

            if (returnData.message && returnData.message.length) {
              var notice = document.createElement('div'),
                  noticeText = document.createTextNode(returnData.message);
              notice.setAttribute('class', 'c-alert c-alert--success c-alert--toast');
              notice.appendChild(noticeText);
              targetEl.appendChild(notice);
              setTimeout(function () {
                targetEl.removeChild(notice);
              }, 5000);
            } // callback(JSON.parse(response), element);

          } else {
            // We reached our target server, but it returned an error
            console.log('Events could not be retrieved.');
          }
        };

        request.onerror = function () {
          // There was a connection error of some sort
          console.log('Connection error while retrieving events.');
        };

        request.send(formData);
      }
    });
  }

  slider.init({
    autoPlay: 6000
  }); // Support legacy content page galleries

  slider.init({
    sliderElement: '.js-gallery',
    autoPlay: 6000,
    contain: true,
    wrapAround: true,
    imagesLoaded: true,
    cellSelector: '.app-gallery-cell',
    cellAlign: 'left'
  }); // Load Slider Resize

  window.addEventListener('load', function () {
    var sliders = Array.prototype.slice.call(document.querySelectorAll('.js-slider-resize'));

    if (sliders) {
      sliders.forEach(function (slider) {
        var flkty = Flickity.data(slider);
        flkty.resize();
      });
    }
  });
});