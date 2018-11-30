package main

import (
  "bufio"
  "fmt"
  "io/ioutil"
  "net/http"
  "os"
  "regexp"
  "sort"
  "strconv"
  "strings"
  "time"
)

type Vid struct {
  Name string
  Date string
  Title string
  Link string
}

func Parse(text string) []Vid {
  n0 := strings.Index(text, "<name>") + 6
  n1 := strings.Index(text, "</name>")
  n := text[n0:n1]
  var dat [45]string

  re := regexp.MustCompile("published>(.*)T")
  found := re.FindAllStringSubmatch(text, -1)
  for f := range found {
    if f == 0 {
	  continue
	}
    dat[f] = found[f][1]
  }
  re = regexp.MustCompile("title>(.*)</ti")
  found = re.FindAllStringSubmatch(text, -1)
  for f := range found {
    if f == 0 {
	  continue
	}
	dat[f+15] = found[f][1]
  }
  re = regexp.MustCompile("(https://www.youtube.com/watch.*)\"")
  found = re.FindAllStringSubmatch(text, -1)
  for f := range found {
	dat[f+30] = found[f][1]
  }
  
  var R []Vid
  for f := 0; f < 15; f++ {
    A := Vid{n, dat[f], dat[f+15], dat[f+30]}
	R = append(R, A)
  }
  return R
}

func main() {
  feed := "https://www.youtube.com/feeds/videos.xml?channel_id="
  d, _ := strconv.Atoi(time.Now().AddDate(0, 0, -7).Format("20060102"))
  file, _ := ioutil.ReadFile("subs.txt")
  lines := strings.Split(string(file), "\n")
  
  var dat []Vid
  
  for x := range lines {
    if x+1 != len(lines) {
	  l := len(lines[x])
	  lines[x] = lines[x][:l-1]
	}
	y := strings.Split(lines[x], "|")
	fmt.Printf("Retrieving videos from " + y[0] + "\r")
	
	resp, _ := http.Get(feed + y[1])
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	t := string(body)
	
	dat = append(dat, Parse(t)...)
  }
  
  sort.Slice(dat, func(i, j int) bool {return dat[i].Date < dat[j].Date})
  for y := range dat {
    dt, _ := strconv.Atoi(strings.Replace(dat[y].Date, "-", "", -1))
	if dt > d {
	  fmt.Println(dat[y].Name + " - " + dat[y].Title + ", " + dat[y].Date + " " + dat[y].Link)
	}
  }
  
  fmt.Printf("\nPress enter to exit.")
  bufio.NewReader(os.Stdin).ReadBytes('\n')
}