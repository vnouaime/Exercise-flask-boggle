class BoggleGame {
  constructor(secs = 60) {
    this.words = new Set();
    this.secs = secs;
    this.showTimer();
    this.score = 0;

    this.timer = setInterval(this.countdown.bind(this), 1000);
    $('#add-word').on("submit", this.checkWord.bind(this));
  }

  /* updates and shows timer */
  showTimer() {
    const $timer = $("#timer");
    $timer.text(this.secs)
  }

  /* updates and shows current user's score */
  showScore() {
    const $score = $("#score")
    $score.text(this.score);
  }

  /* shows differet messages based on the response it receives from the server */
  showMessage(msg) {
    const messages = $("#messages");
    messages.text(msg);
  
  }

  /* updates and shows current user's list of words after it has been validated by the server */
  showWord(word) {
    const $list_of_words = $("#list_of_words")
    const $new_word = $("<li>").text(word)
  
    $list_of_words.append($new_word)
  }

  /* Sends get request to server to check if a word is valid on the board. Then, displays messages depending on the response from the server, updates the score, and clears the value from the form */
  async checkWord(evt) {
    evt.preventDefault();
  
    this.$word = $("#word").val()

    if (!this.$word) return;

    if (this.words.has(this.$word)) {
      this.showMessage(`Already found ${this.$word}`);
      return;
    }

    const response = await axios.get("/check-word", { params: { word: this.$word }});
    const result = response.data.result;

    if (result === "not-word") {
      this.showMessage("This is not a valid word!");
    
    } else if (result === "not-on-board") {
      this.showMessage("This word is not on this board!")
    
    } else {
      this.words.add(this.$word);
      this.score += this.$word.length;
      this.showScore();
      this.showMessage(`Added: ${this.$word}`)
      this.showWord(this.$word)
    }

    $("#word").val("");
  
  }

  /* makes timer countdown until zero where endGame function will be called to end the game */
  async countdown() {
    this.secs -= 1;
    this.showTimer();

    if (this.secs === 0) {
      clearInterval(this.timer);
      await this.endGame();
    }
  }

  /* hides the form and sends a post request to the server with the user's current score. Displays message if user has beat high score depending on the response received from the post request.  */
  async endGame() {
    $("#add-word").hide();
    
    const response = await axios.post("/post-score", { score: this.score });
    
    if (response.data.newHighScore) {
      this.showMessage(`New High Score: ${this.score}!`);
    } else {
      this.showMessage(`Final score: ${this.score}`);
    }
  }

}












  

