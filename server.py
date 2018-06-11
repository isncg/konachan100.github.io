from flask import Flask, render_template, request
import konachan
app = Flask(__name__)

def filt_post_list(ratings):
    try:
        return [p for p in konachan.postlist if p['rating'] in ratings]
    except Exception as e:
        print('ERROR \\')
        print(konachan.postlist)
        return []

def _index(postlist):
    
    agent=request.headers.get('User-Agent')
    #print(agent)
    if agent is not None and 'Mobile' in agent:
        return render_template('postlist_mobile.html', posts=postlist)

    row=[]
    col=[]
    for i in range(len(postlist)):
        col.append(postlist[i])
        if (i+1)%4==0:
            row.append(col)
            col=[]

    if len(col)>0:
        row.append(col)

   
    return render_template('postlist.html', postrow=row)


@app.route('/')
def index():
    return _index(filt_post_list(['s']))

@app.route('/18x')
def index_18x():
    return _index(filt_post_list(['s','q','e']))

# @app.route('/view/<id>')
# def view(id):
#     pass
# def hello_world():
#     row=[]
#     col=[]
#     for i in range(len(konachan.postlist)):
#         col.append(konachan.postlist[i])
#         if (i+1)%4==0:
#             row.append(col)
#             col=[]

#     if len(col)>0:
#         row.append(col)

#     agent=request.headers.get('User-Agent')
#     print(agent)
#     if 'Mobile' in agent:
#         return render_template('postlist_mobile.html', posts=konachan.postlist)
#     return render_template('postlist.html', postrow=row)



if __name__ == '__main__':
    konachan.start_update_thread()
    app.run(host='0.0.0.0',port=80)



