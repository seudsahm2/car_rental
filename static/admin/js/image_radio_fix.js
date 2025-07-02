document.addEventListener('DOMContentLoaded', function () {
    const enforceSingleSelection = () => {
        const radios = document.querySelectorAll('input[name$="-is_primary"]');
        radios.forEach(radio => {
            radio.addEventListener('change', () => {
                radios.forEach(otherRadio => {
                    if (otherRadio !== radio) {
                        otherRadio.checked = false;
                    }
                });
            });
        });
    };

    enforceSingleSelection();
    document.addEventListener('formset:added', enforceSingleSelection);
});