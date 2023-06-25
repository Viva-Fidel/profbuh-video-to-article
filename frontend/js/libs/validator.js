const form = document.querySelector('.hero-form');
const urlInput = document.querySelector('.hero-form__input_link');
const startInput = document.querySelector('.hero-form__input_start');
const endInput = document.querySelector('.hero-form__input_end');
const inputs = document.querySelectorAll('.hero-form__input');
const checkboxTime = document.querySelector('.checkbox_time');
const inputFields = document.querySelectorAll('.hero-form__input[data-type="numberTime"]');
const checkboxAnnotationLength = document.querySelector('.checkbox_annotation');
const checkboxArticleLength = document.querySelector('.checkbox_article');
const inputScreen = document.querySelector('.hero-form__input_screen');

document.addEventListener('DOMContentLoaded', () => {
    const patterns = {
        youtube: /^(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?|youtube\.com\/live|youtu\.be\/))/,
        numberTime: function (value) {
         return value.replace(/(\d{2})(?=\d)/g, '$1.')
        },
        number: function (value) {
            return value.replace(/\D/g, '');
        },
        numberScreen: function (value) {
            return value.replace(/\D/g, '');
        }
    }





    inputs.forEach(input => {
        input.addEventListener('input', function () {
            let pattern = patterns[input.dataset.type];
            if (input.dataset.type == 'youtube') {
                if (pattern.test(input.value.trim())) {
                    if (this.classList.contains('input-base_error')) {
                        this.classList.remove('input-base_error')
                        this.classList.add('input-base_approve')
                    } else {
                        this.classList.add('input-base_approve')
                    }
                } else {
                    if (this.classList.contains('input-base_approve')) {
                        this.classList.remove('input-base_approve')
                        this.classList.add('input-base_error')
                    } else {
                        this.classList.add('input-base_error')
                    }
                }
            }
            if (input.dataset.type == 'numberTime') {
                let formattedValue = pattern(input.value.trim().slice(0, 8).replace(/\D/g, ''));
                this.value = formattedValue;
                    if (pattern.test(input.value.trim())) {
                        if (this.classList.contains('input-base_error')) {
                            this.classList.remove('input-base_error')
                            this.classList.add('input-base_approve')
                        } else {
                            this.classList.add('input-base_approve')
                        }
                    } else {
                        if (this.classList.contains('input-base_approve')) {
                            this.classList.remove('input-base_approve')
                            this.classList.add('input-base_error')
                        } else {
                            this.classList.add('input-base_error')
                        }
                    }






            }
            if (input.dataset.type == 'number') {
                let formattedValue = pattern(input.value.trim().slice(0, 8));
                this.value = formattedValue;
            }
            if (input.dataset.type == 'numberScreen') {
                let formattedValue = pattern(input.value.trim().slice(0, 2));
                this.value = formattedValue;
            }

        })
        checkboxTime.addEventListener('change', function () {
            const isChecked = this.checked;
            inputFields.forEach(input => {
                input.value = ''; // Сброс значения
                if (isChecked) {
                    input.setAttribute('disabled', ''); // Добавление атрибута disabled
                    input.classList.add('input-base_disabled'); // Добавление класса "disabled"
                } else {
                    input.removeAttribute('disabled'); // Удаление атрибута disabled
                    input.classList.remove('input-base_disabled'); // Добавление класса "disabled"
                }
            });
        });
        if (checkboxTime.checked) {
            inputFields.forEach(input => {
                input.value = ''; // Сброс значения
                input.setAttribute('disabled', '');
                input.classList.add('input-base_disabled');
            });
        }

        checkboxAnnotationLength.addEventListener('change', function () {
            const isChecked = this.checked;
            let inputAnnotation = document.querySelector('.hero-form__input_annotation');
            inputAnnotation.value = ''
            if (isChecked) {
                inputAnnotation.setAttribute('disabled', ''); // Добавление атрибута disabled
                inputAnnotation.classList.add('input-base_disabled'); // Добавление класса "disabled"
            } else {
                inputAnnotation.removeAttribute('disabled'); // Удаление атрибута disabled
                inputAnnotation.classList.remove('input-base_disabled'); // Добавление класса "disabled"
            }

        });


        checkboxArticleLength.addEventListener('change', function () {
            const isChecked = this.checked;
            let inputArticle = document.querySelector('.hero-form__input_article');
            inputArticle.value = ''
            if (isChecked) {
                inputArticle.setAttribute('disabled', ''); // Добавление атрибута disabled
                inputArticle.classList.add('input-base_disabled'); // Добавление класса "disabled"
            } else {
                inputArticle.removeAttribute('disabled'); // Удаление атрибута disabled
                inputArticle.classList.remove('input-base_disabled'); // Добавление класса "disabled"
            }
        });


    })
})



form.addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = checkForm();
    let it = 0;

    for(item in formData){
       if(formData[item] === false || formData[item] === ''){
        it++;
       }
    }
    if(it > 0){
        console.log('Данные не отправлены')

    }else{
        console.log('Форма отправлена')
    }

})


function checkForm() {
    const checkFormData = {
        url: '',
        time: '',
        article: '',
        annotation: '',
        screenSec: '',
    }
    let checkTime = 0;

    if (urlInput.classList.contains('input-base_approve')) {
        checkFormData.url = urlInput.value.trim();
    }
    inputFields.forEach((inp) => {
        if (inp.classList.contains('input-base_disabled')) {
            ++checkTime;
        } else {
            inp.value.trim();
        }
    })
    if (checkboxTime.checked && checkTime === 2) {
        checkFormData.time = true
    } else if ((!checkboxTime.checked && inputFields[0].value.trim() !== '') && (!checkboxTime.checked && inputFields[1].value.trim() !== '')) {
        checkFormData.time = [inputFields[0].value.trim(), inputFields[1].value.trim()]
    } else {
        checkFormData.time = false;
    }

    let inputAnnotation = document.querySelector('.hero-form__input_annotation');
    const checkboxAnnotationLength = document.querySelector('.checkbox_annotation');
    if (checkboxAnnotationLength.checked) {
        checkFormData.annotation = true;
    } else  {
        inputAnnotation.value.trim() !== '' ? (checkFormData.annotation = inputAnnotation.value.trim()) : checkFormData.annotation =  false
    }

    let inputArticle = document.querySelector('.hero-form__input_article');
    if (checkboxArticleLength.checked) {
        checkFormData.article = true;
    } else {
        inputArticle.value.trim() !== '' ? checkFormData.article = inputArticle.value.trim() : checkFormData.article = false;
    }
    inputScreen.value.trim() !== '' ? checkFormData.screenSec = inputScreen.value.trim() : checkFormData.screenSec = false ;

    return checkFormData;

}