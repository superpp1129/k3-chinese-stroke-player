(function (cjs, an) {

var p; // shortcut to reference prototypes
var lib={};var ss={};var img={};
lib.ssMetadata = [];


// symbols:



// stage content:
(lib._0001 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer7
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AAYDoIAAmDQgNAOggAQQggAQgbAHIAAg4QAkgKApgVQAogWAWgUIAWAAIAAHPg");
	this.shape.setTransform(72.75,62.3);
	this.shape._off = true;

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(23).to({_off:false},0).wait(12));

	// Layer6
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("AkcFmQikhHishbQnNjzgFheQgGhfAjgWQAjgXBbgMIViiEQDfAnCfA7QEDBgAAB2QAABZluDHIgiASIg4ANQjmA2h5ApQh5AqhaApQhaAqg1AAQg2AAidhEg");
	this.shape_1.setTransform(239.1883,546.4375);

	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#000000").s().p("A6oHvQikhGishcQnNj0gFhdQgGheAjgXQAjgWBbgNMBBogGQIA8gGIBrAUQBqATCjAaQB3AWAwAfQA4AkAABIQAABoisBPQhEAfh7AoIhJAYQzkBmlVA7QkbAwk/A7QmxBQjnA2QjmA1h5ApQh5AqhaApQhbAqg1AAQg2AAidhEg");
	this.shape_2.setTransform(381.1883,532.7);

	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#000000").s().p("EgpKAJfQikhHishbQnNj0gFheQgGhfAjgVQAjgXBbgMMBBogGQQMDhMMYhwIEmgqQDcA/C9BYQD9B1AABIQAAAlggBGQgqBchGBLIgeAeQvugHuNBIQ2WB0lxBAQkbAwlAA7QmxBQjnA1QjmA2h5ApQh5AqhaApQhbAqg1AAQg2AAidhEg");
	this.shape_3.setTransform(474.1883,521.5375);

	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#000000").s().p("EgzgAKkQikhGishbQnMj1gGheQgFheAjgXQAigWBcgNMBBogGPQMDhLMXhwQMYhwCLgWQCLgVBigSQBhgRBtASQBtATCwBbQCwBbDeCLQDeCMAACBQAABVhBA1Qg+A0i4AJQ6GhU2XBzQ2WBzlwBAQkcAwk/A7QmyBQjmA2QjnA1h4AqQh5AphbAqQhaApg2AAQg1AAiehEg");
	this.shape_4.setTransform(540.3133,514.5761);

	this.timeline.addTween(cjs.Tween.get({}).to({state:[]}).to({state:[{t:this.shape_1}]},23).to({state:[{t:this.shape_2}]},3).to({state:[{t:this.shape_3}]},3).to({state:[{t:this.shape_4}]},3).wait(3));

	// Layer4
	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#999999").s().p("EgzgAKkQikhGishbQnMj1gGheQgFheAjgXQAigWBcgNMBBogGPQMDhLMXhwQMYhwCLgWQCLgVBigSQBhgRBtASQBtATCwBbQCwBbDeCLQDeCMAACBQAABVhBA1Qg+A0i4AJQ6GhU2XBzQ2WBzlwBAQkcAwk/A7QmyBQjmA2QjnA1h4AqQh5AphbAqQhaApg2AAQg1AAiehEg");
	this.shape_5.setTransform(540.3133,514.5761);

	this.timeline.addTween(cjs.Tween.get(this.shape_5).wait(35));

	// Layer2
//	this.shape_6 = new cjs.Shape();
//	this.shape_6.graphics.f().s("#FF0000").ss(8,1,1).p("AcI8HMAAAg4QAcIcIMA4QAAAAcI8HMA4QAAAAcIcIMAAAg4PA8H8HMAAAg4QEhUXgcHMA4QAAAEhUXAcIMA4QAAAMAAAg4PMA4PAAAA8HcIMA4PAAAEgcHBUYMAAAg4QEAcIBUYMAAAg4Q");
//	this.shape_6.setTransform(540,540);

//	this.timeline.addTween(cjs.Tween.get(this.shape_6).wait(35));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(520,523,577.2,577.2);
// library properties:
lib.properties = {
	id: '022FE2FC1A6C364CAEBF0B6B7741924F',
	width: 1080,
	height: 1080,
	fps: 24,
	color: "#FFFFFF",
	opacity: 1.00,
	manifest: [],
	preloads: []
};



// bootstrap callback support:

(lib.Stage = function(canvas) {
	createjs.Stage.call(this, canvas);
}).prototype = p = new createjs.Stage();

p.setAutoPlay = function(autoPlay) {
	this.tickEnabled = autoPlay;
}
p.play = function() { this.tickEnabled = true; this.getChildAt(0).gotoAndPlay(this.getTimelinePosition()) }
p.stop = function(ms) { if(ms) this.seek(ms); this.tickEnabled = false; }
p.seek = function(ms) { this.tickEnabled = true; this.getChildAt(0).gotoAndStop(lib.properties.fps * ms / 1000); }
p.getDuration = function() { return this.getChildAt(0).totalFrames / lib.properties.fps * 1000; }

p.getTimelinePosition = function() { return this.getChildAt(0).currentFrame / lib.properties.fps * 1000; }

an.bootcompsLoaded = an.bootcompsLoaded || [];
if(!an.bootstrapListeners) {
	an.bootstrapListeners=[];
}

an.bootstrapCallback=function(fnCallback) {
	an.bootstrapListeners.push(fnCallback);
	if(an.bootcompsLoaded.length > 0) {
		for(var i=0; i<an.bootcompsLoaded.length; ++i) {
			fnCallback(an.bootcompsLoaded[i]);
		}
	}
};

an.compositions = an.compositions || {};
an.compositions['022FE2FC1A6C364CAEBF0B6B7741924F'] = {
	getStage: function() { return exportRoot.getStage(); },
	getLibrary: function() { return lib; },
	getSpriteSheet: function() { return ss; },
	getImages: function() { return img; }
};

an.compositionLoaded = function(id) {
	an.bootcompsLoaded.push(id);
	for(var j=0; j<an.bootstrapListeners.length; j++) {
		an.bootstrapListeners[j](id);
	}
}

an.getComposition = function(id) {
	return an.compositions[id];
}


an.makeResponsive = function(isResp, respDim, isScale, scaleType, domContainers) {		
	var lastW, lastH, lastS=1;		
	window.addEventListener('resize', resizeCanvas);		
	resizeCanvas();		
	function resizeCanvas() {			
		var w = lib.properties.width, h = lib.properties.height;			
		var iw = window.innerWidth, ih=window.innerHeight;			
		var pRatio = window.devicePixelRatio || 1, xRatio=iw/w, yRatio=ih/h, sRatio=1;			
		if(isResp) {                
			if((respDim=='width'&&lastW==iw) || (respDim=='height'&&lastH==ih)) {                    
				sRatio = lastS;                
			}				
			else if(!isScale) {					
				if(iw<w || ih<h)						
					sRatio = Math.min(xRatio, yRatio);				
			}				
			else if(scaleType==1) {					
				sRatio = Math.min(xRatio, yRatio);				
			}				
			else if(scaleType==2) {					
				sRatio = Math.max(xRatio, yRatio);				
			}			
		}			
		domContainers[0].width = w * pRatio * sRatio;			
		domContainers[0].height = h * pRatio * sRatio;			
		domContainers.forEach(function(container) {				
			container.style.width = w * sRatio + 'px';				
			container.style.height = h * sRatio + 'px';			
		});			
		stage.scaleX = pRatio*sRatio;			
		stage.scaleY = pRatio*sRatio;			
		lastW = iw; lastH = ih; lastS = sRatio;            
		stage.tickOnUpdate = false;            
		stage.update();            
		stage.tickOnUpdate = true;		
	}
}


})(createjs = createjs||{}, AdobeAn = AdobeAn||{});
var createjs, AdobeAn;