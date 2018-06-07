!function() {
    function star() {
        var starData=[];
        var starBgData=[];
        var starRMin = 10;
        var starZMax = 3000;
        var starZStep = 10;
        var starMaxCnt = 800;
        var starBgMaxCnt = 300;

        var starMaxColor = 150;
        var starMinColor = 40;

        var starBgMaxColor = 80;
        var starBgMinColor = 40;
        //var cWidth = 600;
        //var cHeight = 600;
        var cWidth = document.body.scrollWidth;
        var cHeight = document.body.scrollHeight;
        var starEl = document.createElement('canvas');
        var starDiv = document.getElementById('bgStar');
        starEl.style.backgroundColor = '#000000';
        starEl.setAttribute("width", cWidth);
        starEl.setAttribute("height", cHeight);
        starDiv.appendChild(starEl);
        var ctx = starEl.getContext("2d");
        var ctxI = ctx.getImageData(0,0,cWidth,cHeight);
        var ctxData = ctxI.data;

        createData();
        startMove();
        window.addEventListener("resize", addResizeEvent);

        function getRandomXYZ(rMin, d, maxz, minColor, maxColor) {
            var x = Math.random()*d - d/2;
            var y = Math.random()*d - d/2;
            var z = Math.round(Math.random()*maxz);
            var c = minColor + Math.round(Math.random()*(maxColor-minColor));
            if(rMin <= 0)
                return;
            for(;Math.sqrt(x*x, y*y) < rMin;) {
                x = Math.random()*d - d/2;
                y = Math.random()*d - d/2;
            }
            return { x:x, y:y, z:z, x2d:0, y2d:0, c:c}
        }

        function createData() {
            var i,tmpData,width;
            width = (cWidth > cHeight) ? cWidth : cHeight;

            for(i = 0; i < starBgMaxCnt; i++) {
                tmpData = getRandomXYZ(starRMin, width, starZMax, starBgMinColor, starBgMaxColor);
                starBgData.push(tmpData);
            }

            for(i = 0; i < starMaxCnt; i++) {
                tmpData = getRandomXYZ(starRMin, width, starZMax, starMinColor, starMaxColor);
                starData.push(tmpData);
            }
        }

        function convertData() {
            var i,t,k;
            for(i=0; i<starBgData.length; i++) {
                t = starBgData[i];
                k = 1500/(1500+t.z);
                t.x2d = Math.floor(t.x*k);
                t.y2d = Math.floor(t.y*k);
                writeToCanvas(t);
            }
            for(i=0; i<starData.length; i++) {
                t = starData[i];
                t.z -= starZStep;
                if(t.z < -400) {
                    t.z = starZMax;
                }
                k = 800/(800+t.z);
                t.x2d = Math.floor(t.x*k);
                t.y2d = Math.floor(t.y*k);
                writeToCanvas(t);
            }
        }
        
        function writeToCanvas(data){
            var index,w,h;
            w = Math.round(cWidth/2);
            h = Math.round(cHeight/2);
            if((data.x2d>w)||(data.x2d<-w)||(data.y2d>h)||(data.y2d<-h)){
                return;
            }
            index = 4*((w+data.x2d)+(h+data.y2d)*cWidth);
            ctxData[index] = data.c; 
            ctxData[index+1] = data.c; 
            ctxData[index+2] = data.c; 
            ctxData[index+3] = 0xff; 
        }

        function clearCanvas() {
            for(var i=0; i<ctxData.length; i+=4) {
               ctxData[i] = 0; 
               ctxData[i+1] = 0; 
               ctxData[i+2] = 0; 
               ctxData[i+3] = 0xff; 
            }
        }

        function updateCanvas() {
            clearCanvas();
            convertData();
            ctx.putImageData(ctxI, 0, 0);
        }

        function addResizeEvent() {
            //cWidth = window.innerWidth;
            //cHeight = window.innerHeight;
            cWidth = document.body.scrollWidth;
            cHeight = document.body.scrollHeight;
			console.log("width:" + cWidth);
			console.log("height:" + cHeight);
            starEl.setAttribute("width", cWidth);
            starEl.setAttribute("height", cHeight);
            ctxI = ctx.getImageData(0,0,cWidth,cHeight);
            ctxData = ctxI.data;
        }

        function startMove() {
            window.requestAnimationFrame(startMove);
            updateCanvas();
        }
    }
    window.bgStar = star
}();
