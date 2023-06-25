const form = document.querySelector('.hero-form');
const inputs = form.querySelectorAll('.hero-form__input');
const checkboxTime = document.querySelector('.checkbox_time');
const checkboxAnnotation = document.querySelector('.checkbox_annotation');
const checkboxArticleLength = document.querySelector('.checkbox_article');
// patterns
const patterns = {
    youtube: /^(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?|youtube\.com\/live|youtu\.be\/))/,
    numberTime: function (value) {
        return value.replace(/(\d{2})(?=\d)/g, '$1.')
    },
    number: function (value) {
        return value.replace(/\D/g, '');
    },
    screen: function (value) {
        return value.replace(/\D/g, '');
    }
}

console.log(`     / \\__
    (    @\\___
    /         O
   /   (_____/
  /_____/   U


  <Bublik the pug/>
  `


  );



document.addEventListener('DOMContentLoaded', () => {
    inputs.forEach((inp) => {
        inp.addEventListener('input', () => {
            if (inp.dataset.type === 'youtube') {
                checkUrlInput(inp)
            } else if (inp.dataset.type == 'numberTime') {
                checkTimesInput(inp)
                debugger
            } else if (inp.dataset.type == 'number') {
                checkNumberInput(inp);
            } else if (inp.dataset.type == 'screen') {
                checkScreenInput(inp);
            }
        })
    })


    if (checkboxTime.checked) {
        setDisabled(document.querySelector('.hero-form__input_start'), document.querySelector('.hero-form__input_end'))
        clearValue(document.querySelector('.hero-form__input_start'), document.querySelector('.hero-form__input_end'))
    } else {
        removeDisabled(document.querySelector('.hero-form__input_start'), document.querySelector('.hero-form__input_end'))
    }

    if (checkboxAnnotation.checked) {
        setDisabled(document.querySelector('.hero-form__input_annotation'))
        clearValue(document.querySelector('.hero-form__input_annotation'))
    } else {
        removeDisabled(document.querySelector('.hero-form__input_annotation'))
    }
    if (checkboxArticleLength.checked) {
        setDisabled(document.querySelector('.hero-form__input_article'))
        clearValue(document.querySelector('.hero-form__input_article'))
    } else {
        removeDisabled(document.querySelector('.hero-form__input_article'))
    }


    form.addEventListener('submit', (e) => {
        e.preventDefault()
    })


    function checkUrlInput(input) {
        const classes = {
            approve: 'input-base_approve',
            error: 'input-base_error',
        }
        let purgEvalue = input.value.trim();
        let pattern = patterns[input.dataset.type];
        let resultTest = pattern.test(purgEvalue)
        if (resultTest) {
            if (input.classList.contains(classes.error)) {
                input.classList.remove(classes.error);
                input.classList.add(classes.approve);
                removeMessage(input.dataset.type)
            } else{
                input.classList.add(classes.approve);
                removeMessage(input.dataset.type)
            }
        } else if (!resultTest) {
            input.classList.add(classes.error);
            input.classList.contains(classes.approve) ? input.classList.remove(classes.approve) : '';
            setMessage(input.dataset.type)

        }

    }




    function checkTimesInput(input) {
        if (input.type === 'checkbox') {
            if (input.checked) {
                setDisabled(document.querySelector('.hero-form__input_start'), document.querySelector('.hero-form__input_end'))
                clearValue(document.querySelector('.hero-form__input_start'), document.querySelector('.hero-form__input_end'))
                removeMessage(document.querySelector('.hero-form__input_start').dataset.type, document.querySelector('.hero-form__input_start'))
                removeMessage(document.querySelector('.hero-form__input_end').dataset.type, document.querySelector('.hero-form__input_end'))
            } else {
                removeDisabled(document.querySelector('.hero-form__input_start'), document.querySelector('.hero-form__input_end'))
            }
        }
        const classes = {
            approve: 'input-base_approve',
            error: 'input-base_error',
        }
        let purgEvalue = input.value.trim();
        if (/[a-zA-Z]/.test(purgEvalue)) {
            purgEvalue = purgEvalue.replace(/[a-zA-Z]/g, '');
            input.value = purgEvalue;
            return;
        }
        let pattern = patterns[input.dataset.type];
        let formattedValue = pattern(purgEvalue.trim().slice(0, 8).replace(/\D/g, ''));
        input.value = formattedValue;
        if (input.value.length == 8 || input.value.length == 0) {
            removeMessage(input.dataset.type, input)
        } else if (input.value.length < 8) {
            setMessage(input.dataset.type, input)
        }
    }

    function checkScreenInput(input) {
        let purgEvalue = input.value.trim();
        if (/[a-zA-Z]/.test(purgEvalue)) {
            // Удаление букв из значения
            purgEvalue = purgEvalue.replace(/[a-zA-Z]/g, '');
            input.value = purgEvalue;
            return;
        }
        let pattern = patterns[input.dataset.type];
        let formattedValue = pattern(input.value.trim().slice(0, 2));
        this.value = formattedValue;
    }

    function checkNumberInput(input) {
        if (input.type === 'checkbox') {
            if (input.classList.contains('checkbox_annotation')) {
                if (input.checked) {
                    setDisabled(document.querySelector('.hero-form__input_annotation'));
                    clearValue(document.querySelector('.hero-form__input_annotation'))
                    removeMessage(document.querySelector('.hero-form__input_annotation').dataset.type, document.querySelector('.hero-form__input_annotation'))
                } else {
                    removeDisabled(document.querySelector('.hero-form__input_annotation'))
                }
            }
            if (input.classList.contains('checkbox_article')) {
                if (input.checked) {
                    setDisabled(document.querySelector('.hero-form__input_article'));
                    clearValue(document.querySelector('.hero-form__input_article'))
                    removeMessage(document.querySelector('.hero-form__input_article').dataset.type, document.querySelector('.hero-form__input_article'))

                }else{
                    removeDisabled(document.querySelector('.hero-form__input_article'))

                }
            }
        }


        let pattern = patterns[input.dataset.type];
        let formattedValue = pattern(input.value.trim().slice(0, 8));
        input.value = formattedValue;
    }

    function setMessage(inputType, inp) {
        const errorItemYouTube = document.querySelector('.error-text_youtube');
        const errorItemnumberTimeStart = document.querySelector('.error-text_numberTime_start');
        const errorItemnumberTimeEnd = document.querySelector('.error-text_numberTime_end');

        const messageBook = {
            youtube: 'пожалуйста,введите корректную ссылку',
            numberTime: 'пожалуйста,придерживайтесь формата [чч.мм.сс]',
        }
        if (inputType === 'youtube') {
            errorItemYouTube.classList.add('error-text_active')
            errorItemYouTube.textContent = messageBook[inputType];
        } else if (inputType === 'numberTime') {
            if (inp.classList.contains('hero-form__input_start')) {
                errorItemnumberTimeStart.classList.add('error-text_active')
                errorItemnumberTimeStart.textContent = messageBook[inputType];
            } else if (inp.classList.contains('hero-form__input_end')) {
                errorItemnumberTimeEnd.classList.add('error-text_active')
                errorItemnumberTimeEnd.textContent = messageBook[inputType];
            }

        }
    }

    function removeMessage(inputType, inp) {
        const errorItemYouTube = document.querySelector('.error-text_youtube');
        const errorItemnumberTimeStart = document.querySelector('.error-text_numberTime_start');
        const errorItemnumberTimeEnd = document.querySelector('.error-text_numberTime_end');
        if (inputType === 'youtube') {
            errorItemYouTube.classList.remove('error-text_active')
            errorItemYouTube.textContent = '';
        } else if (inputType === 'numberTime') {
            if (inp.classList.contains('hero-form__input_start')) {
                errorItemnumberTimeStart.classList.remove('error-text_active')
                errorItemnumberTimeStart.textContent = '';
            } else if (inp.classList.contains('hero-form__input_end')) {
                errorItemnumberTimeEnd.classList.remove('error-text_active')
                errorItemnumberTimeEnd.textContent = '';
            }
        }
    }

    function setDisabled(...inputs) {
        inputs.forEach(inp => {
            inp.classList.add('input-base_disabled');
            inp.setAttribute('disabled', '');
        })
    }

    function removeDisabled(...inputs) {
        inputs.forEach(inp => {
            inp.classList.remove('input-base_disabled');
            inp.removeAttribute('disabled');
        })
    }

    function clearValue(...inputs) {
        inputs.forEach(inp => {
            inp.value = '';
        })
    }
})
