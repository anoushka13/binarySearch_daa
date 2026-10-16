import sys, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgb
from matplotlib.animation import FuncAnimation, FFMpegWriter

NAVY="#1F3864"; ORANGE="#F4B942"; DORANGE="#C77800"; GREEN="#2E9E5B"
LB="#DCE6F7"; GREY="#CFCFCF"; RED="#C0392B"; DG="#888888"
FPS=24
fig=plt.figure(figsize=(12.8,7.2),dpi=100)
ax=fig.add_axes([0,0,1,1])

def clamp(x): return max(0.0,min(1.0,x))
def seg(t,a,b): return clamp((t-a)/(b-a))
def ease(x): return x*x*(3-2*x)
def mix(c1,c2,k):
    a=np.array(to_rgb(c1)); b=np.array(to_rgb(c2)); return tuple(a*(1-k)+b*k)
def T(x,y,s,size=20,color=NAVY,alpha=1.0,weight="normal",ha="center"):
    if alpha<=0.01: return
    ax.text(x,y,s,fontsize=size,color=color,alpha=alpha,fontweight=weight,ha=ha,va="center")
def box(x,y,w,h,fc,ec=NAVY,lw=2.0):
    ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fc=fc,ec=ec,lw=lw))

A=[2,5,8,12,16,23,38,56,72,91]
def make_steps(key):
    lo,hi=0,len(A)-1; steps=[]
    while lo<=hi:
        mid=lo+(hi-lo)//2; steps.append((lo,hi,mid))
        if A[mid]==key: break
        elif A[mid]<key: lo=mid+1
        else: hi=mid-1
    return steps,(lo,hi)

# ------------------------------------------------ scenes
def title(tl):
    T(8,6.4,"Binary Search",58,NAVY,ease(seg(tl,0.2,1.2)),"bold")
    ax.add_patch(Rectangle((3,5.35),10*ease(seg(tl,0.6,1.6)),0.06,fc=NAVY,ec="none"))
    T(8,4.6,"Divide and Conquer",32,DORANGE,ease(seg(tl,1.0,2.0)),"bold")
    a=ease(seg(tl,1.6,2.6))
    T(8,2.6,"Design and Analysis of Algorithms (CSEG3053)",18,NAVY,a)
    T(8,2.0,"Anoushka Chawla  |  SAP ID 590022992  |  Batch B18",18,NAVY,a)
    T(8,1.4,"UPES, Dehradun",16,DG,a)

GUESSES=[(50,"Higher!"),(75,"Lower!"),(62,"Higher!"),(68,"Correct!")]
def gx(v): return 1+(v-0.5)/100*14
def guess(tl):
    T(8,8.1,"Warm-up: a guessing game",34,NAVY,ease(seg(tl,0.2,0.9)),"bold")
    T(8,7.1,"I'm thinking of a number between 1 and 100.",20,NAVY,ease(seg(tl,0.6,1.3)))
    T(8,6.5,"You may only ask: is it higher or lower?",20,NAVY,ease(seg(tl,1.0,1.7)))
    y=3.4
    ax.add_patch(Rectangle((1,y-.45),14,.9,fc=GREY,ec=NAVY,lw=2))
    D=2.5; lo,hi=1,100; disp=(1,100); cur=None
    for i,(g,ans) in enumerate(GUESSES):
        s=2.0+i*D
        if ans=="Higher!": nlo,nhi=g+1,hi
        elif ans=="Lower!": nlo,nhi=lo,g-1
        else: nlo,nhi=lo,hi
        if tl>=s:
            k=ease(seg(tl,s+1.7,s+2.3))
            disp=(lo+(nlo-lo)*k, hi+(nhi-hi)*k); cur=(g,ans,s)
        lo,hi=nlo,nhi
    x0=1+(disp[0]-1)/100*14; x1=1+disp[1]/100*14
    ax.add_patch(Rectangle((x0,y-.45),max(x1-x0,0.05),.9,fc=LB,ec=NAVY,lw=2))
    T(1,y-1.0,"1",16,DG); T(15,y-1.0,"100",16,DG)
    T(x0,y-1.0,f"{int(round(disp[0]))}",16,NAVY,ha="center",weight="bold") if tl>2.5 else None
    T(x1,y-1.5,f"{int(round(disp[1]))}",16,NAVY,ha="center",weight="bold") if tl>2.5 else None
    if cur:
        g,ans,s=cur; l=tl-s
        if l<2.4:
            gxp=gx(g)
            ax.plot([gxp,gxp],[y-.6,y+.9],color=DORANGE,lw=4)
            T(gxp,y+1.35,f"Is it {g}?",22,DORANGE,ease(seg(l,0,0.4)),"bold")
            col=GREEN if ans=="Correct!" else RED
            T(gxp,y+2.0,ans,24,col,ease(seg(l,0.9,1.3)),"bold")
    if tl>12.3:
        a=ease(seg(tl,12.3,13.0))
        T(8,1.5,"Found in just 4 guesses!",28,GREEN,a,"bold")
        T(8,0.8,"Every answer cuts the possibilities in half:  100 \u2192 50 \u2192 25 \u2192 12 \u2192 6 ...",18,NAVY,a)

def search(tl,key,Ds,intro,head):
    steps,final=make_steps(key); n=len(steps)
    found=(A[steps[-1][2]]==key)
    T(8,8.4,head,30,NAVY,1,"bold")
    T(8,7.6,f"Sorted array of n = 10 numbers.  Key = {key}",20,NAVY,ease(seg(tl,0.3,1.0)))
    y=4.7; xs=[1.8+1.4*i for i in range(10)]
    grey=[0.0]*10; cur=None
    for i,(lo,hi,mid) in enumerate(steps):
        s=intro+i*Ds
        if A[mid]==key: disc=[]
        elif A[mid]<key: disc=range(lo,mid+1)
        else: disc=range(mid,hi+1)
        if s<=tl<s+Ds: cur=(i,tl-s,lo,hi,mid)
        k=ease(seg(tl,s+0.62*Ds,s+0.85*Ds))
        for j in disc: grey[j]=max(grey[j],k)
    last=steps[-1]; s_last=intro+(n-1)*Ds
    green_on = found and tl>=s_last+0.55*Ds
    fa=ease(seg(tl,0.5,1.2))
    for j in range(10):
        fc=mix(LB,GREY,grey[j])
        if cur and j==cur[4] and cur[1]>=0.18*Ds: fc=mix(ORANGE,GREY,grey[j])
        if green_on and j==last[2]: fc=GREEN
        box(xs[j],y,1.25,1.25,fc)
        T(xs[j],y,str(A[j]),22,mix(NAVY,DG,grey[j]) if not(green_on and j==last[2]) else "white",fa,"bold")
        T(xs[j],y-1.1,str(j),14,DG,fa)
    n_txt=f"n = 10"
    # pointers
    if tl<intro:
        a=ease(seg(tl,1.2,1.8))
        T(xs[0],y+1.0,"lo",18,NAVY,a,"bold"); T(xs[9],y+1.0,"hi",18,NAVY,a,"bold")
        T(8,2.3,"lo = 0,   hi = n - 1 = 9",22,NAVY,ease(seg(tl,1.6,2.2)))
        T(8,1.5,"Idea: compare the key with the MIDDLE element and throw half away.",18,DORANGE,ease(seg(tl,2.2,2.8)),"bold")
    if cur:
        i,l,lo,hi,mid=cur
        a=ease(seg(l,0,0.1*Ds))
        lab="lo,hi" if lo==hi else None
        if lab: T(xs[lo],y+1.0,"lo = hi",18,NAVY,a,"bold")
        else:
            T(xs[lo],y+1.0,"lo",18,NAVY,a,"bold"); T(xs[hi],y+1.0,"hi",18,NAVY,a,"bold")
        T(xs[mid],y+1.7,"mid",20,DORANGE,ease(seg(l,0.18*Ds,0.26*Ds)),"bold")
        T(8,2.5,f"mid = lo + (hi - lo) / 2 = {lo} + ({hi} - {lo}) / 2 = {mid}",20,NAVY,ease(seg(l,0.18*Ds,0.28*Ds)))
        v=A[mid]
        rel="<" if v<key else (">" if v>key else "=")
        T(8,1.75,f"Compare:  a[{mid}] = {v}   {rel}   {key}",22,NAVY,ease(seg(l,0.38*Ds,0.48*Ds)),"bold")
        if v==key: msg,col=f"Equal!  Found it at index {mid}.",GREEN
        elif v<key: msg,col=f"{v} < {key}: key is on the RIGHT.  Discard left half,  lo = mid + 1 = {mid+1}",RED
        else: msg,col=f"{v} > {key}: key is on the LEFT.  Discard right half,  hi = mid - 1 = {mid-1}",RED
        T(8,1.0,msg,19,col,ease(seg(l,0.55*Ds,0.65*Ds)),"bold")
        T(14.6,6.7,f"Comparisons: {i+1}",18,DORANGE,ease(seg(l,0.38*Ds,0.48*Ds)),"bold",ha="right")
    end=intro+n*Ds
    if tl>=end:
        a=ease(seg(tl,end,end+0.6))
        T(14.6,6.7,f"Comparisons: {n}",18,DORANGE,1,"bold",ha="right")
        if found:
            T(8,2.2,f"FOUND  {key}  at index {last[2]}  after only {n} comparisons",26,GREEN,a,"bold")
            T(8,1.4,"(Linear search would have needed 6.)",18,NAVY,a)
        else:
            T(8,2.2,f"lo = {final[0]} is greater than hi = {final[1]}  ->  the range is empty",22,RED,a,"bold")
            T(8,1.4,f"{key} is NOT in the array  ({n} comparisons)",24,RED,a,"bold")

COUNTS=[(10,4),(100,7),(1000,10),(10000,14),(100000,17),(1000000,20)]
def complexity(tl):
    T(8,8.4,"How fast is it?",34,NAVY,ease(seg(tl,0.2,0.9)),"bold")
    T(8,7.4,r"$T(n)=T(n/2)+\Theta(1)\;\Rightarrow\;T(n)=\Theta(\log n)$",30,NAVY,ease(seg(tl,0.8,1.8)))
    ha=ease(seg(tl,1.6,2.2))
    T(3.0,6.2,"n  (elements)",18,DG,ha,"bold"); T(7.2,6.2,"Linear search",18,RED,ha,"bold"); T(11.0,6.2,"Binary search",18,GREEN,ha,"bold")
    for i,(nn,c) in enumerate(COUNTS):
        s=2.4+i*1.15; y=5.3-0.78*i; a=ease(seg(tl,s,s+0.4))
        T(3.0,y,f"{nn:,}",20,NAVY,a,"bold")
        T(7.2,y,f"{nn:,}",20,RED,a)
        w=0.17*c*ease(seg(tl,s+0.2,s+0.9))
        if a>0.01:
            ax.add_patch(Rectangle((9.0,y-.22),w,.44,fc=GREEN,ec="none",alpha=a))
            T(9.0+w+0.15,y,str(c),18,GREEN,ease(seg(tl,s+0.7,s+1.0)),"bold",ha="left")
    a=ease(seg(tl,9.6,10.4))
    T(8,0.75,"1,000,000 elements  ->  only 20 comparisons!   (floor(log2 n) + 1)",22,GREEN,a,"bold")

def outro(tl):
    T(8,7.8,"Key takeaways",36,NAVY,ease(seg(tl,0.2,0.9)),"bold")
    items=["1.  The array must be SORTED (and allow random access).",
           "2.  Each comparison halves the search range.",
           "3.  Time  O(log n)   |   Space  O(1) iterative."]
    for i,t in enumerate(items):
        T(8,6.0-1.1*i,t,24,NAVY,ease(seg(tl,0.9+i*1.2,1.6+i*1.2)),"bold")
    a=ease(seg(tl,4.8,5.6))
    T(8,2.2,"Full C implementation: binary_search.c",20,DORANGE,a,"bold")
    T(8,1.5,"Anoushka Chawla  |  590022992  |  UPES",16,DG,a)

SCENES=[(4.0,title),(15.5,guess),
        (24.5,lambda t:search(t,23,6.0,3.0,"Binary search: a successful search")),
        (23.6,lambda t:search(t,40,4.4,2.5,"Binary search: an unsuccessful search")),
        (13.5,complexity),(8.0,outro)]
starts=np.cumsum([0]+[d for d,_ in SCENES])
TOTAL=starts[-1]

def render(t):
    ax.clear(); ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")
    for i,(d,f) in enumerate(SCENES):
        if starts[i]<=t<starts[i+1] or (i==len(SCENES)-1 and t>=starts[i]):
            tl=t-starts[i]; f(tl)
            fade=1-ease(seg(tl,0,0.35)) if i>0 else 0
            fo=ease(seg(tl,d-0.35,d)) if i<len(SCENES)-1 else 0
            al=max(fade,fo)
            if al>0.01: ax.add_patch(Rectangle((0,0),16,9,fc="white",ec="none",alpha=al,zorder=100))
            break

if __name__=="__main__":
    if sys.argv[1]=="test":
        for t in map(float,sys.argv[2:]):
            render(t); fig.savefig(f"t_{t:05.1f}.png")
    else:
        n=int(TOTAL*FPS)
        anim=FuncAnimation(fig,lambda k:render(k/FPS),frames=n,interval=1000/FPS)
        w=FFMpegWriter(fps=FPS,codec="libx264",extra_args=["-pix_fmt","yuv420p","-crf","20","-preset","medium"])
        anim.save("binary_search_explainer.mp4",writer=w,progress_callback=lambda i,n:print(i,n,flush=True) if i%100==0 else None)
        print("DONE",flush=True)
