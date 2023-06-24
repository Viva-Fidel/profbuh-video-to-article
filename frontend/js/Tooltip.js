import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';
/* hero-form questions */
const heroQuestion = document.querySelectorAll('.hero-form__question');
const heroQuestionTooltipBox = document.querySelectorAll('.hero-form__tooltip-box');

console.log(heroQuestionTooltipBox);
for(let i=0; i <heroQuestion.length;i++){
tippy(heroQuestion[i], {
    content: heroQuestionTooltipBox[i].innerHTML,
    allowHTML: true,
    placement: 'top',
    animation: 'fade',
    delay: [150, 300],
    interactiveBorder: 30,
    theme: 'white',
    interactive: true,
    interactiveDebounce: 75,

  });
}
