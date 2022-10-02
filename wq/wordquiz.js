/*************
This is Fisher-Yates
shuffle algorithm implementation from
http://sedition.com/perl/javascript-fy.html
*************/

function shuffle( myArray ) {
  var i = myArray.length;
  if ( i == 0 ) return false;
  while ( --i ) {
     var j = Math.floor( Math.random() * ( i + 1 ) );
     var tempi = myArray[i];
     var tempj = myArray[j];
     myArray[i] = tempj;
     myArray[j] = tempi;
   }
}

function arrIndexOf(arr, item) {
    for(var i=0; i<arr.length;i++) {
	if (item == arr[i]) {
	    return i;
	}
    }
    return -1;
}

/****************************************
 object WordQuiz(n)

 Multichoise quiz, n is the number of choices

 we assume gobal variables:
 wlist - WordList object containing ductionary
 langs - list of langauges used in wlist

 methods:
 setLangs(lang1, lang2) - lang 1 is used for questions and lang2 for answers
 getStrings() - returns list of string used in quiz, item[0] is the question
****************************************/
function WordQuiz(n) {
    this.setLangs = function(q_lang, a_lang) {
	this.q_lang = q_lang;
	this.a_lang = a_lang;
    };

    this.getQString = function() {
	//document.writeln("<br>" + this.q_lang + " - " + this.q_word + "<br>");
	return wlist.getWord(this.q_word, this.q_lang);
    };

    this.getAStrings = function() {
	var r = new Array();
	for(var i=0; i < this.a_num; i++) {
	    r.push(wlist.getWord(this.a_words[i], this.a_lang));
	}
	return r;
    };

    this.getStrings = function() {
	var r = new Array(this.getQString());
	return r.concat(this.getAStrings());
    };

    this.nextWord = function() {
	if(this.keys.length == 0) {
	    this.keys = wlist.getKeys();
	}
	var all_keys = new Array();
	all_keys = wlist.getKeys();
	shuffle(all_keys);

	shuffle(this.keys);
	this.q_word = this.keys[0];
	this.keys.splice(0,1);

	var i = arrIndexOf(all_keys, this.q_word);
	
	all_keys.splice(i, 1);

	this.a_words = all_keys.slice(0, this.a_num - 1);
	this.a_words.push(this.q_word);
	shuffle(this.a_words);
	this.right_answer = arrIndexOf(this.a_words, this.q_word);
    };
    
    this.isRight = function(n) {
	return (n == this.right_answer);
    }

    this.keys = wlist.getKeys();

    this.q_lang = ""; // language used to ask words
    this.q_word = null; // 

    this.a_num = n; // how many choices
    this.a_lang = ""; // language used in answers
    this.a_words = []; // multichoice words, including right answer
    this.right_answer = -1; // index in a_words containing right answer
}


/****************************************
 object WordList

 contains list of words in different languages
 each word is identified by key string

 methods:
 
 addWord(key) - creates new empty word with key
 setWord(key, lang, word) - e.g. setWord("tab", "English", "table")
                            if key doesn't exist in WordList creates
                            new Word object with addWord method
 getWordObject(key) - returns corresponding Word object
 getWord(key, lang) - returns corresponding word string
                       e.g. getWord("tab", "English") returns "table"
 getKeys() - returns list of existing keys
 getRandom() - returns random key from WordList
 getRandomSlice(n) - returns random n-length list of keys from WordList,
                      no duplicates
****************************************/
function WordList() {
    this.getWordObject = function(key) {
	for (var i=0; i<this.word_list.length; i++) 
	{
            if (this.word_list[i].key == key) {
		return this.word_list[i];
	    }
	}
	return null;
    };

    this.addWord = function(key) {
	if (this.getWordObject(key) != null) {
	    return;
	}
	this.word_list.push(new Word(key));
    };

    this.getWord = function(key, lang) {
	var w = this.getWordObject(key);
	if  (w == null) {
	    return null;
	}
	return w.getWord(lang);
    };

    this.setWord = function(key, lang, word) {
	this.addWord(key);
	w = this.getWordObject(key);
	w.setWord(lang, word);
    };

    this.getKeys = function() {
	var keys = new Array();
	for (var i=0; i<this.word_list.length; i++) {
	    keys.push(this.word_list[i].key);
	}
	return keys;
    };

    this.getRandom = function() {
	var keys = this.getKeys();
	return  keys[Math.round((Math.random() * keys.length))]
    };

    this.getRandomSlice = function(n) {
	var r = new Array()
	var keys = this.getKeys();
	shuffle(keys);
	r = keys.slice(0,n);
	return r;
    }
    this.word_list = new Array();
      
}
/****************************************
 object Word

 constructor is gived argument 'key' which identifies the word
 setWord(lang, word) method can be used to add or modify words
                     (e.g. setWord("English", "table")
 getWord(lang) returns the word in given lang
                     (getWord("English") returns "table"

****************************************/
function Word(key) {
    this.setWord = function(lang, word) {
	this[lang] = word;
    }

    this.getWord = function(lang) {
	return this[lang];
    }

    this.key=key;
}


