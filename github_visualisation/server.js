
const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');


let langData= fs.readFileSync('data/lang.json');
let reposData = fs.readFileSync('data/repos.json');
let userData = fs.readFileSync('data/users.json');
let commitData = fs.readFileSync('data/commits.json');
let repo_contributors = fs.readFileSync('data/repo_contributors.json');


let lang_list = JSON.parse(langData);
let repo_list = JSON.parse(reposData);
let user_list = JSON.parse(userData);
let commit_list = JSON.parse(commitData);
let repo_cont = JSON.parse(repo_contributors);
var chart_json;



//console.log(langList);
const app = express()


makeGraphData("flutter-webrtc","All",commit_list,repo_cont);

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


function makeGraphData(repo, login, commit_list,repo_contributors) {
  var graph_json;


  if(repo.trim() == "All" && login.trim() == "All") { // removing extra whitespace for comparison
      // add all user logins as Node(user), add all repos as Repo(user)
      // for each commit to a repo add a link source : commit.login,  target = commit.repo_name, value

  }
  else if(repo.trim() == "All") {



  }
  else if(login.trim() == "All") {
    var dataArray = []
    var nodes = []
    var links = []

    var commitList = []
    var count =0;
    var count2 =0;
    var index = repo_contributors.length;
    while(index--) {
      if(repo_contributors[index].repo_name == repo) {
          // found user that commits in given repo

          for(var key in commit_list) {
            if(commit_list[key].login== repo_contributors[index].login && commit_list[key].repo_name == repo) {
              // found users commit in given repo
              count2++;

            }

          }

          commitList[count] = count2;
          count2 =0


          nodes.push({"name": repo_contributors[index].login , "group": 0});
          count++;
      }

    }
    console.log(count)
    nodes.push({"name":repo, "group": 1});
      // finished pushing all nodes, there are |count| nodes + 1 (the repo)
    for(var i = 0; i < count ; i++) {
        links.push({"source":i, "target":count, "value":commitList[i]});
    }

    dataArray.push({"nodes": nodes, "links": links});


      dataArray = dataArray[0];
  //  let dataJSON = JSON.stringify(dataArray);
  //  fs.writeFileSync('test2.json', dataJSON);
      graph_json = dataArray;




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

  //  let dataJSON = JSON.stringify(dataArray);
  // fs.writeFileSync('test1.json', dataJSON);

    graph_json = dataArray;


  }



  return graph_json;


}
