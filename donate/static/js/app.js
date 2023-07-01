function fundations_contains_categories() {
    const cat_check = document.querySelectorAll('#step1 .form-group--checkbox input');
    const found_check = document.querySelectorAll('#step3 .form-group--checkbox input');

    function list_of_checked_categories() {
        let lst = [];
        cat_check.forEach(element => {
            if (element.checked == true) {
                lst.push(element.value);
            }
        })
        return lst;
    }

    function hide_others_foundations(lst) {
        found_check.forEach(element => {
            element.parentElement.parentElement.classList.remove('hide');
            let categories = element.dataset.categories.split(',');
            lst.forEach(num => {
                if (!categories.includes(num)) {
                    element.parentElement.parentElement.classList.add('hide');
                }
            })

        })
    }

    cat_check.forEach(e => {
        e.addEventListener('change', function (event) {
            let lst = list_of_checked_categories();
            hide_others_foundations(lst);
        })
    })
}

document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.$buttonsContainerPaginator1 = $el.querySelector('#pagi1');
            this.$buttonsContainerPaginator2 = $el.querySelector('#pagi2');
            this.$buttonsContainerPaginator3 = $el.querySelector('#pagi3');
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target;

            // Buttons Active class change
            if ([...this.$buttonsContainerPaginator1.children].includes(page.parentElement)) {
                [...this.$buttonsContainerPaginator1.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
                page.classList.add("active");
                this.changeContent(page, this.currentSlide)

            }
            if ([...this.$buttonsContainerPaginator2.children].includes(page.parentElement)) {
                [...this.$buttonsContainerPaginator2.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
                page.classList.add("active");
                this.changeContent(page, this.currentSlide)
            }
            if ([...this.$buttonsContainerPaginator3.children].includes(page.parentElement)) {
                [...this.$buttonsContainerPaginator3.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
                page.classList.add("active");
                this.changeContent(page, this.currentSlide)
            }


        }

        changeContent(page, type) {
            const ul = page.parentElement.parentElement.parentElement.querySelector('.help--slides-items');
            ul.innerHTML = '';
            this.getData(page.dataset.page, type - 1).then(data => createContent(data, ul));
        }

        getData(page, type) {
            const my_url = '/donate/inst-api/?page=' + page + '&type=' + type;
            return fetch(my_url).then(response => response.json())
        }
    }

    function createContent(data, ul) {
        data.forEach(element => {
            let li = document.createElement('li');

            let div1 = document.createElement('div');
            div1.classList.add('col');
            let div_title = document.createElement('div');
            div_title.classList.add('title');
            div_title.innerText = 'Fundacja ' + element.name;
            let div_subtitle = document.createElement('div');
            div_subtitle.classList.add('subtitle');
            div_subtitle.innerText = 'Cel i misja: ' + element.description;
            div1.appendChild(div_title);
            div1.appendChild(div_subtitle);


            let div2 = document.createElement('div');
            div2.classList.add('col');
            let div_text = document.createElement('div');
            div_text.classList.add('text');
            div_text.innerText = element.categories;
            div2.appendChild(div_text);

            li.appendChild(div1);
            li.appendChild(div2);
            ul.appendChild(li);
        });
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => {
                this.submit(e)
            });
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            // e.preventDefault();
            // this.currentStep++;
            // this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }

    fundations_contains_categories();

    const cat_check = document.querySelectorAll('#step1 .form-group--checkbox input');
    const found_check = document.querySelectorAll('#step3 .form-group--checkbox input');
    const last_button = document.querySelector('#last-step');
    const quantity = document.querySelector('#id_quantity');
    const address = document.querySelector('#id_address');
    const city = document.querySelector('#id_city');
    const zip_code = document.querySelector('#id_zip_code');
    const phone_number = document.querySelector('#id_phone_number');
    const pick_up_date = document.querySelector('#id_pick_up_date');
    const pick_up_time = document.querySelector('#id_pick_up_time');
    const pick_up_comment = document.querySelector('#id_pick_up_comment');
    const donation_categories = document.querySelector('#donation_categories');
    const donation_foundation = document.querySelector('#donation_foundation');
    const donation_address = document.querySelector('#donation_address');
    const donation_date = document.querySelector('#donation_date');



    last_button.addEventListener('click', function (){

        let categories = [];
        let foundation = [];
        let comment = pick_up_comment.value;
        if (!comment){comment = 'Brak uwag'}

        cat_check.forEach(element => {
            if(element.checked == true){
                categories.push(element.parentElement.lastElementChild.innerText);
            }
        })
        found_check.forEach(element => {
            if(element.checked == true){
                foundation.push(element.parentElement.querySelector('.title').innerText);
            }
        })

        foundation = foundation[0].split(' ').slice(1).join(' ');

        categories = categories.slice(0, categories.length-2).map(e => e+',').concat(categories.slice(categories.length-2, categories.length)); // add comas to categories
        if (categories.length > 1){categories.splice(categories.length-1, 0, 'oraz');} // add 'oraz' before last element
        categories = categories.join(' ');

        if (quantity.value == 1){
            donation_categories.innerText = 'Worek zawierający ' + categories;
        }
        else{
            donation_categories.innerText = quantity.value + ' worki zawierające ' + categories;
        }

        donation_foundation.innerText = 'Dla fundacji ' + foundation;


        donation_address.innerHTML = '';
        let li_address = document.createElement('li');
        li_address.innerText = address.value;
        let li_city = document.createElement('li');
        li_city.innerText = city.value;
        let li_zip_code = document.createElement('li');
        li_zip_code.innerText = zip_code.value;
        let li_phone_number = document.createElement('li');
        li_phone_number.innerText = phone_number.value;
        donation_address.appendChild(li_address);
        donation_address.appendChild(li_city);
        donation_address.appendChild(li_zip_code);
        donation_address.appendChild(li_phone_number);


        donation_date.innerHTML = '';
        let li_date = document.createElement('li');
        li_date.innerText = pick_up_date.value;
        let li_time = document.createElement('li');
        li_time.innerText = pick_up_time.value;
        let li_comment = document.createElement('li');
        li_comment.innerText = comment;

        donation_date.appendChild(li_date);
        donation_date.appendChild(li_time);
        donation_date.appendChild(li_comment);




    })

});
