/* ==========================================================================
   Landing page — JavaScript
   Scroll reveal, counter animation, navbar scroll, floating particles
   ========================================================================== */

(function () {
  "use strict";

  // ---- Scroll-reveal via IntersectionObserver ----
  function initReveal() {
    var els = document.querySelectorAll(".reveal");
    if (!els.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    els.forEach(function (el) { observer.observe(el); });
  }

  // ---- Animated counter ----
  function animateCounter(el) {
    var target = parseInt(el.getAttribute("data-target"), 10);
    var suffix = el.getAttribute("data-suffix") || "";
    var duration = 2000;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      // Ease-out cubic
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(eased * target) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  function initCounters() {
    var counters = document.querySelectorAll("[data-counter]");
    if (!counters.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounter(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach(function (el) { observer.observe(el); });
  }

  // ---- Navbar scroll effect ----
  function initNavbar() {
    var nav = document.querySelector(".navbar");
    if (!nav) return;

    function onScroll() {
      if (window.scrollY > 60) {
        nav.classList.add("scrolled");
      } else {
        nav.classList.remove("scrolled");
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ---- Mobile nav toggle ----
  function initNavToggle() {
    var toggle = document.querySelector(".nav-toggle");
    var links = document.querySelector(".nav-links");
    if (!toggle || !links) return;

    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
    // Close on link click
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("open");
      });
    });
  }

  // ---- Floating particles ----
  function initParticles() {
    var container = document.querySelector(".hero-particles");
    if (!container) return;

    var colors = ["particle--gold", "particle--sage", "particle--blush"];

    for (var i = 0; i < 20; i++) {
      var p = document.createElement("div");
      p.className = "particle " + colors[i % colors.length];
      var size = 4 + Math.random() * 10;
      p.style.width = size + "px";
      p.style.height = size + "px";
      p.style.left = Math.random() * 100 + "%";
      p.style.animationDuration = (8 + Math.random() * 14) + "s";
      p.style.animationDelay = (Math.random() * 12) + "s";
      container.appendChild(p);
    }
  }

  // ---- Smooth scroll for anchor links ----
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        // href="#" murni bukan pemilih yang sah; querySelector("#") melempar
        // SyntaxError dan menghentikan penanganan klik berikutnya.
        var tujuan = a.getAttribute("href");
        if (!tujuan || tujuan === "#") return;
        var target = document.querySelector(tujuan);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
  }

  // ---- Init ----
  document.addEventListener("DOMContentLoaded", function () {
    initNavbar();
    initNavToggle();
    initParticles();
    initReveal();
    initCounters();
    initSmoothScroll();
  });
})();
