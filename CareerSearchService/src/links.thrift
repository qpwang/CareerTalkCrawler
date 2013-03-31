namespace py CareerSearch.gen

enum Status {
  	SUCCEED = 0,
  	FAIL = 1,
  	FOUND = 2,
  	REDIRECT = 3
}

enum LinkType {
	UNKNOWN = 0,
	CATELOG = 1,
	LEAF = 2
}

struct Link {
	1: string url
}

struct LinkPredicate {
	1: string source
}

struct LinkStatus {
	1: string url
	2: string source
	3: Status status
	4: LinkType type
	5: i32 pages
}

service Links {
    list<Link> getLinks(1:LinkPredicate predicate, 2:i32 pendings)
    void reportStatus(1:list<LinkStatus> statusList)
}