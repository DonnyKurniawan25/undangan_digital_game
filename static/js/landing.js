/* ==========================================================================
   Jelajah Undangan — Landing Page Interactive Engine
   ========================================================================== */

(function () {
  "use strict";

  // ---- 1. Scroll Reveal Animations ----
  function initScrollReveal() {
    var revealElements = document.querySelectorAll(".reveal");
    if (!revealElements.length) return;

    // Check if IntersectionObserver is supported
    if ("IntersectionObserver" in window) {
      var revealObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
              revealObserver.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
      );

      revealElements.forEach(function (el) {
        revealObserver.observe(el);
      });
    } else {
      // Fallback for older browsers
      revealElements.forEach(function (el) {
        el.classList.add("visible");
      });
    }
  }

  // ---- 2. Animated Numerical Counters ----
  function animateCounter(el) {
    var target = parseInt(el.getAttribute("data-target"), 10) || 0;
    var suffix = el.getAttribute("data-suffix") || "";
    var duration = 1800; // ms
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      // Easing: easeOutExpo
      var eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      var currentVal = Math.floor(eased * target);
      el.textContent = currentVal.toLocaleString("id-ID") + suffix;

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target.toLocaleString("id-ID") + suffix;
      }
    }

    requestAnimationFrame(step);
  }

  function initCounters() {
    var counters = document.querySelectorAll("[data-counter]");
    if (!counters.length) return;

    if ("IntersectionObserver" in window) {
      var counterObserver = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              animateCounter(entry.target);
              counterObserver.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.4 }
      );

      counters.forEach(function (el) {
        counterObserver.observe(el);
      });
    } else {
      counters.forEach(function (el) {
        animateCounter(el);
      });
    }
  }

  // ---- 3. Glassmorphic Navbar on Scroll ----
  function initNavbar() {
    var navbar = document.getElementById("navbar");
    if (!navbar) return;

    function handleScroll() {
      if (window.scrollY > 40) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    }

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll();
  }

  // ---- 4. Mobile Navigation Drawer Toggle ----
  function initMobileNav() {
    var toggleBtn = document.getElementById("nav-toggle");
    var navLinks = document.getElementById("nav-links");
    if (!toggleBtn || !navLinks) return;

    function toggleMenu() {
      var isOpen = navLinks.classList.contains("open");
      if (isOpen) {
        navLinks.classList.remove("open");
        toggleBtn.classList.remove("open");
        document.body.style.overflow = "";
      } else {
        navLinks.classList.add("open");
        toggleBtn.classList.add("open");
        document.body.style.overflow = "hidden";
      }
    }

    toggleBtn.addEventListener("click", toggleMenu);

    // Close on navigation link click
    var links = navLinks.querySelectorAll("a");
    links.forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
        toggleBtn.classList.remove("open");
        document.body.style.overflow = "";
      });
    });

    // Close when clicking outside
    document.addEventListener("click", function (e) {
      if (navLinks.classList.contains("open") && !navLinks.contains(e.target) && !toggleBtn.contains(e.target)) {
        navLinks.classList.remove("open");
        toggleBtn.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  }

  // ---- 5. Interactive Theme Filter ----
  function initThemeFilter() {
    var filterButtons = document.querySelectorAll(".theme-filter-btn");
    var themeCards = document.querySelectorAll(".theme-card");
    if (!filterButtons.length || !themeCards.length) return;

    filterButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var filter = btn.getAttribute("data-filter");

        // Set active button
        filterButtons.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");

        // Filter cards
        themeCards.forEach(function (card) {
          var category = card.getAttribute("data-category");
          if (filter === "all" || category === filter) {
            card.style.display = "flex";
            setTimeout(function () {
              card.style.opacity = "1";
              card.style.transform = "translateY(0)";
            }, 50);
          } else {
            card.style.opacity = "0";
            card.style.transform = "translateY(20px)";
            setTimeout(function () {
              card.style.display = "none";
            }, 300);
          }
        });
      });
    });
  }

  // ---- 6. FAQ Accordion Engine ----
  function initFAQ() {
    var faqItems = document.querySelectorAll(".faq-item");
    if (!faqItems.length) return;

    faqItems.forEach(function (item) {
      var questionBtn = item.querySelector(".faq-question");
      var answer = item.querySelector(".faq-answer");
      if (!questionBtn || !answer) return;

      questionBtn.addEventListener("click", function () {
        var isActive = item.classList.contains("active");

        // Optional: close other accordions
        faqItems.forEach(function (otherItem) {
          if (otherItem !== item && otherItem.classList.contains("active")) {
            otherItem.classList.remove("active");
            var otherAnswer = otherItem.querySelector(".faq-answer");
            if (otherAnswer) otherAnswer.style.maxHeight = null;
            var otherBtn = otherItem.querySelector(".faq-question");
            if (otherBtn) otherBtn.setAttribute("aria-expanded", "false");
          }
        });

        if (isActive) {
          item.classList.remove("active");
          answer.style.maxHeight = null;
          questionBtn.setAttribute("aria-expanded", "false");
        } else {
          item.classList.add("active");
          answer.style.maxHeight = answer.scrollHeight + 30 + "px";
          questionBtn.setAttribute("aria-expanded", "true");
        }
      });
    });
  }

  // ---- Initialize All Modules on DOM Ready ----
  document.addEventListener("DOMContentLoaded", function () {
    initScrollReveal();
    initCounters();
    initNavbar();
    initMobileNav();
    initThemeFilter();
    initFAQ();
  });
})();
