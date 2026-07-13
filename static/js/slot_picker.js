document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll(".slot-btn");

    const hidden = document.getElementById("id_time_slot");

    const dateInput = document.getElementById("id_appointment_date");

    buttons.forEach(btn => {

        btn.addEventListener("click", function () {

            if (btn.classList.contains("booked")) {

                return;

            }

            buttons.forEach(b => b.classList.remove("active"));

            btn.classList.add("active");

            hidden.value = btn.dataset.slot;

        });

    });

    if (!dateInput) return;

    dateInput.addEventListener("change", function () {

        fetch(

            window.location.pathname.replace("/book/", "/booked-slots/") +

            "?date=" + dateInput.value

        )

        .then(response => response.json())

        .then(data => {

            buttons.forEach(btn => {

                btn.classList.remove("booked");

                btn.disabled = false;

                btn.innerHTML = btn.dataset.slot;

            });

            data.booked_slots.forEach(slot => {

                buttons.forEach(btn => {

                    if (btn.dataset.slot === slot) {

                        btn.classList.add("booked");

                        btn.disabled = true;

                        btn.innerHTML = "❌ " + slot;

                    }

                });

            });

        });

    });

});