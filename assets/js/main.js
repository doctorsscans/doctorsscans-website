/* ==========================================================================
   Doctors Scans & Labs — main.js

   One job: when someone taps a "Book on WhatsApp" button, ask which centre
   they want, then open WhatsApp for that centre with the message ready.

   Nothing on this site depends on JavaScript to be readable. If this file
   fails to load, every page still shows all of its content, and every branch
   page still has a direct WhatsApp link and a phone number.
   ========================================================================== */
(function () {
  "use strict";

  var BASE = "Hello Doctors Scans, I would like to book";

  function openWhatsApp(number, what) {
    var msg = BASE + " " + what + ".";
    window.open(
      "https://wa.me/" + number + "?text=" + encodeURIComponent(msg),
      "_blank",
      "noopener"
    );
  }

  document.addEventListener("DOMContentLoaded", function () {
    var modalEl = document.getElementById("branchPicker");
    if (!modalEl) return;

    // If Bootstrap failed to load, send people to the branches page instead of
    // leaving the buttons dead.
    if (typeof bootstrap === "undefined" || !bootstrap.Modal) {
      document.addEventListener("click", function (e) {
        var t = e.target.closest("[data-book]");
        if (!t) return;
        e.preventDefault();
        window.location.href = "/branches/";
      });
      return;
    }

    var modal = new bootstrap.Modal(modalEl);
    var pending = "an appointment";

    // Any element with data-book opens the picker
    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-book]");
      if (!trigger) return;
      e.preventDefault();
      pending = trigger.getAttribute("data-book") || "an appointment";

      // A service may only be offered at some centres. Show just those.
      var scope = trigger.getAttribute("data-at");
      var allowed = scope ? scope.split(",") : null;
      var shown = [];
      modalEl.querySelectorAll(".picker-item").forEach(function (item) {
        var ok = !allowed || allowed.indexOf(item.getAttribute("data-slug")) !== -1;
        item.hidden = !ok;
        if (ok) shown.push(item);
      });

      // Only one centre offers it — skip the picker and open WhatsApp directly.
      if (shown.length === 1) {
        openWhatsApp(shown[0].getAttribute("data-wa"), pending);
        return;
      }

      var label = modalEl.querySelector("#branchPickerLabel");
      if (label) {
        label.textContent =
          pending === "an appointment"
            ? "Which centre would you like?"
            : "Where would you like " + pending + "?";
      }
      modal.show();
    });

    // Picking a centre opens that centre's WhatsApp
    modalEl.addEventListener("click", function (e) {
      var item = e.target.closest(".picker-item");
      if (!item) return;
      e.preventDefault();
      var num = item.getAttribute("data-wa");
      modal.hide();
      openWhatsApp(num, pending);
    });
  });
})();
