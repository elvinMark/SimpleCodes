function turingMachine(blank,str_states,str_transitions,tape_len){
    this.b = blank;
    this.q = eval(str_states);
    this.t = JSON.parse(str_transitions);
    this.tape_len = tape_len;
    this.initial_state = this.q[0];
    this.final_state = this.q[this.q.length - 1];
    this.curr_state = this.initial_state;
    this.tape = [];
    for(var i = 0;i<tape_len;i++)
	this.tape.push(blank);

    this.head = Math.floor(this.tape_len/2);
    this.history = [];

    this.states_pos = [];
    //Methods
    this.set_input = function(str_in){
	for(var i = 0;i<str_in.length;i++)
	    this.tape[this.head+i] = str_in[i];
    };
    this.print_curr_state = function(){
	s = "Current State: " + this.curr_state + "\n";
	for(var i =0;i<this.tape_len;i++){
	    s = s + this.tape[i] +" ";
	}
	s  = s + "\n";
	for(var i =0;i<this.tape_len;i++){
	    if(i == this.head)
		s = s + "^" + " ";
	    else
		s = s + " " + " ";
	}
	console.log(s);
	this.history.push(s);
    };
    this.run = function(){
	var instr;
	this.history = []; //store all the steps
	while(this.curr_state != this.final_state){
	    this.print_curr_state();
	    instr = this.t[this.curr_state][this.tape[this.head]];
	    this.tape[this.head] = instr[0];
	    if(instr[1] == 'R')//go right
		this.head += 1;
	    else if(instr[1] == 'L')//go left
		this.head -= 1;
	    else
		continue;
	    this.curr_state = instr[2];
	}
	this.print_curr_state();
}
    this.get_state_index = function(state){
	var i = 0;
	while(this.q[i]!=state){
	    i++;
	    if(i== this.q.length)
		return -1;
	}
	return i;
    }
    this.draw_machine = function(ctx,H,W){
	var cx = W/2;
	var cy = H/2;
	var d = Math.min(H,W);
	var r = 0.4*d
	var cr = 0.08*d;
	var ns = this.q.length;
	var dtheta = 2*Math.PI/ns;
	var s1,s2;
	var nc;
	for(var i in this.q){
	    ctx.beginPath();
	    this.states_pos.push(new vector(cx+r*Math.cos(i*dtheta),cy+r*Math.sin(i*dtheta)));
	    ctx.arc(this.states_pos[i].x,this.states_pos[i].y,cr,0,2*Math.PI);
	    ctx.stroke();
	    ctx.font = "20px Arial";
	    ctx.fillText(this.q[i],this.states_pos[i].x - 5*this.q[i].length,this.states_pos[i].y);
	}
	for(var i in this.t){
	    s1 = this.get_state_index(i);
	    for(var j in this.t[i]){
		s2 = this.get_state_index(this.t[i][j][2]);
		if(s1 == s2){
		    continue;
		}
		else{
		    nc = get_center(this.states_pos[s1],this.states_pos[s2],r*Math.abs(s2-s1),s2>s1?1:-1);
		    ctx.beginPath();
		    ctx.arc(nc.x,nc.y,r*Math.abs(s2-s1),get_angle(this.states_pos[s1],nc),get_angle(this.states_pos[s2],nc));
		    ctx.stroke();
		}
	    }
	}
    }
}

function vector(x,y){
    this.x = x;
    this.y = y;
    this.tangent = function(){
	return new vector(-this.y,this.x);
    };
    this.norm = function(){
	return Math.sqrt(this.x*this.x + this.y*this.y);
    };
    this.diff = function (v){
	return new vector(this.x - v.x,this.y - v.y);
    };
    this.sum = function (v){
	return new vector(this.x + v.x,this.y + v.y);
    };
    this.times = function(num){
	return new vector(this.x*num,this.y*num);
    };
    this.normalize = function(){
	var s = this.norm();
	this.x = this.x/s;
	this.y = this.y/s;
    };
}

function get_center(v1,v2,R,opt){
    var a;
    a = Math.sqrt(R**2 - v2.diff(v1).norm()/4);
    var u = v2.diff(v1).tangent();
    u.normalize();
    a = opt*a;
    return v2.sum(v1).times(0.5).sum(u.times(a));
}

function get_angle(p,c){
    return (p.x>0?Math.PI:0) + Math.atan((p.y-c.y)/(p.x-c.x));
}
