// static/admin/js/image_radio_fix.js

document.addEventListener('DOMContentLoaded', function () {
    const updateRadioNames = () => {
        const radios = document.querySelectorAll('input[name$="-is_primary"]');
        radios.forEach(radio => {
            radio.setAttribute('name', 'primary_image'); // make all share one group
        });
    };

    updateRadioNames(); // initial load

    document.addEventListener('formset:added', updateRadioNames); // dynamic forms
});
