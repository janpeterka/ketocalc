Stimulus.register("daily-plan", class extends Controller {
  static get targets() {
    return ["percentage"]
  }

  set_amount(event){
      // var percentage = 100;

        if (event != undefined){
          event.preventDefault();
          var target = event.target
          if ("percentage" in target.dataset){
            this.percentageTarget.value = target.dataset.percentage;
          }
        }
  }

});
