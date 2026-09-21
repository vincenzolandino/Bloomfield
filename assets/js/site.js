(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var reduceMotion = false;
  try {
    reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) {
    reduceMotion = false;
  }

  if (reduceMotion) {
    root.classList.add("reduce-motion");
  }

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    requestAnimationFrame(function () {
      root.classList.add("is-ready");
    });

    var header = document.querySelector("[data-header]");
    if (header) {
      var updateHeader = function () {
        header.classList.toggle("is-scrolled", window.scrollY > 8);
      };
      updateHeader();
      window.addEventListener("scroll", updateHeader, { passive: true });
    }

    var revealNodes = document.querySelectorAll("[data-reveal]");
    if (!revealNodes.length) {
      return;
    }

    var show = function (node) {
      node.classList.add("is-in");
    };

    if (reduceMotion || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(revealNodes, show);
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            show(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );

    Array.prototype.forEach.call(revealNodes, function (node) {
      observer.observe(node);
    });
  });
})();
