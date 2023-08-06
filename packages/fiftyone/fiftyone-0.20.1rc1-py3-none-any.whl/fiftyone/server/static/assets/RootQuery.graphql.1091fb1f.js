const r=function(){var a={defaultValue:null,kind:"LocalArgument",name:"count"},e={defaultValue:null,kind:"LocalArgument",name:"cursor"},n={defaultValue:"",kind:"LocalArgument",name:"search"},l=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}];return{fragment:{argumentDefinitions:[a,e,n],kind:"Fragment",metadata:null,name:"RootQuery",selections:[{args:null,kind:"FragmentSpread",name:"RootDatasets_query"},{args:null,kind:"FragmentSpread",name:"RootGA_query"},{args:null,kind:"FragmentSpread",name:"RootNav_query"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[n,a,e],kind:"Operation",name:"RootQuery",selections:[{alias:null,args:l,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:l,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"},{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"teamsSubmission",storageKey:null}]},params:{cacheID:"fdc459a58a769462216652fec0f50846",id:null,metadata:{},name:"RootQuery",operationKind:"query",text:`query RootQuery(
  $search: String = ""
  $count: Int
  $cursor: String
) {
  ...RootDatasets_query
  ...RootGA_query
  ...RootNav_query
}

fragment RootDatasets_query on Query {
  datasets(search: $search, first: $count, after: $cursor) {
    total
    edges {
      cursor
      node {
        name
        id
        __typename
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}

fragment RootGA_query on Query {
  context
  dev
  doNotTrack
  uid
  version
}

fragment RootNav_query on Query {
  teamsSubmission
}
`}}}();r.hash="1d7f694b7f4950c7d7917f3b274f084d";export{r as default};
