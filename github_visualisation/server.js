
const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');


let langData= fs.readFileSync('data/lang.json');
let reposData = fs.readFileSync('data/repos.json');
let userData = fs.readFileSync('data/users.json');
let commitData = fs.readFileSync('data/commits.json');


let lang_list = JSON.parse(langData);
let repo_list = JSON.parse(reposData);
let user_list = JSON.parse(userData);
let commit_list = JSON.parse(commitData);
var chart_json;



//console.log(langList);
const app = express()


makeGraphData("flutter-webrtc","cloudwebrtc",commit_list);

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs')

app.get('/', function (req, res) {
  chart_json = makeChartData("All","All",commit_list);
  graph_json = makeChartData("All","All",commit_list);
  res.render('index', {langList: lang_list,reposList:repo_list,userList:user_list});
})
app.post('/', function (req, res) {
  chart_json = makeChartData("All","All",commit_list);
  graph_json = makeChartData("All","All",commit_list);
  res.render('index', {langList: lang_list,reposList:repo_list,userList:user_list});
})



app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})



function makeChartData(repo, login, commit_list) {
    var chart_json;
    var temp_list = commit_list;
    if(repo.trim() == "All" && login.trim() == "All") { // removing extra whitespace for comparison
        chart_json = commit_list;

    }
    else if(repo.trim() == "All") {
      // all repos of one user case
      var i =temp_list.length;
      while(i--) {

        if (temp_list[i].login != login) {
          // remove from resulting json
          var removed = temp_list.splice(i, 1);
        }
      }
      chart_json = temp_list;


    }
    else if(login.trim() == "All") {
      // all users 1 repo case

      var i =temp_list.length;
      while(i--) {

        if (temp_list[i].repo_name != repo) {
          // remove from resulting json
          var removed = temp_list.splice(i, 1);
        }
      }

      chart_json = temp_list;

    }
    else {
      // repo and login are single values case
      var i =temp_list.length;
      while(i--) {

        if (temp_list[i].repo_name != repo) {
          // remove from resulting json
          var removed = temp_list.splice(i, 1);
        }
        else if(temp_list[i].login != login) {
          var removed = temp_list.splice(i, 1);
        }
      }
      chart_json = temp_list;

    }
  //let data = JSON.stringify(chart_json);
  //fs.writeFileSync('test_1_repo_1_user.json', data);
    return chart_json;
}


function makeGraphData(repo, login, commit_list) {
  var graph_json;
  if(repo.trim() == "All" && login.trim() == "All") { // removing extra whitespace for comparison
      // add all user logins as Node(user), add all repos as Repo(user)
      // for each commit to a repo add a link source : commit.login,  target = commit.repo_name, value

  }
  else if(repo.trim() == "All") {



  }
  else if(login.trim() == "All") {
    // all users 1 repo case


  }
  else {
    // repo and login are single values case
    var dataArray = []
    var nodes = []
    var links = []

    nodes.push({"name":login, "group": 0});
    nodes.push({"name":repo, "group": 1});

    links.push({"source": 0, "target": 1, "value": 1});



    dataArray.push({"nodes":nodes, "links": links});





    var dataArray = dataArray[0];
    let dataJSON = JSON.stringify(dataArray);
    fs.writeFileSync('test1.json', dataJSON);





  }



  return graph_json;


}
