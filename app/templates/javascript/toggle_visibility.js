<script src="https://unpkg.com/stimulus/dist/stimulus.umd.js"></script>

<script type="text/javascript">
  const application = Stimulus.Application.start()

  application.register("password-visibility", class extends Stimulus.Controller {
    static get targets() {
      return ["password"]
    }

  connect() {
    this._add_icon()
  }

  _add_icon(){
    var html='<span class="fa fa-fw fa-eye field-icon" data-action="mouseover->password-visibility#turnOnVisibility mouseout->password-visibility#turnOffVisibility"></span>'

    $(this.passwordTarget).append(html)
  }

  turnOnVisibility(e) {
  	const x = $('#password');
    x.attr("type", 'text');
  }

  turnOffVisibility(e) {
  	const x = $('#password');
    x.attr("type", 'password');
  }
})
</script>
