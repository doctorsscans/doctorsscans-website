/* ==========================================================================
   Doctors Scans & Labs — main.js

   Two jobs, both using the same centre-picker popup:
   - "Book on WhatsApp" / "WhatsApp" buttons ask which centre, then open
     WhatsApp for that centre with the message ready.
   - "Call" buttons ask which centre, then open the phone dialer for that
     centre's number.

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

  function openCall(tel) {
    window.location.href = "tel:" + tel;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var modalEl = document.getElementById("branchPicker");
    if (!modalEl) return;

    // If Bootstrap failed to load, send people to the branches page instead of
    // leaving the buttons dead.
    if (typeof bootstrap === "undefined" || !bootstrap.Modal) {
      document.addEventListener("click", function (e) {
        var t = e.target.closest("[data-book], [data-call]");
        if (!t) return;
        e.preventDefault();
        window.location.href = "/branches/";
      });
      return;
    }

    var modal = new bootstrap.Modal(modalEl);
    var pending = "an appointment"; // message text, used only in whatsapp mode
    var mode = "whatsapp"; // "whatsapp" or "call"

    // Any element with data-book or data-call opens the picker
    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-book], [data-call]");
      if (!trigger) return;
      e.preventDefault();

      mode = trigger.hasAttribute("data-call") ? "call" : "whatsapp";
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

      // Only one centre offers it — skip the picker and act directly.
      if (shown.length === 1) {
        if (mode === "call") {
          openCall(shown[0].getAttribute("data-tel"));
        } else {
          openWhatsApp(shown[0].getAttribute("data-wa"), pending);
        }
        return;
      }

      var label = modalEl.querySelector("#branchPickerLabel");
      if (label) {
        if (mode === "call") {
          label.textContent = "Which centre would you like to call?";
        } else {
          label.textContent =
            pending === "an appointment"
              ? "Which centre would you like?"
              : "Where would you like " + pending + "?";
        }
      }
      modal.show();
    });

    // Picking a centre acts on that centre, per the mode that opened the picker
    modalEl.addEventListener("click", function (e) {
      var item = e.target.closest(".picker-item");
      if (!item) return;
      e.preventDefault();
      modal.hide();
      if (mode === "call") {
        openCall(item.getAttribute("data-tel"));
      } else {
        openWhatsApp(item.getAttribute("data-wa"), pending);
      }
    });
  });
})();
