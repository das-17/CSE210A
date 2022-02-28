datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

function flatten<T>(tree:Tree<T>):List<T>
{
	match tree
    case Leaf => Nil
    case Node(LTree, RTree, value) => append(flatten(LTree),append(Cons(value,Nil), flatten(RTree)))
}


function append<T>(xs:List<T>, ys:List<T>):List<T>
ensures xs == Nil ==> append(xs, ys) == ys
ensures ys == Nil ==> append(xs, ys) == xs
{
    match xs
    case Nil => ys
    case Cons(x,xs') => Cons(x, append(xs',ys))
}

function treeContains<T>(tree:Tree<T>, element:T):bool
{
	match tree
    case Leaf => false
    case Node(LTree, RTree, value) => treeContains(LTree, element) || treeContains(RTree, element) || (value == element)
}


function listContains<T>(xs:List<T>, element:T):bool
{
	match xs
    case Nil => false
    case Cons(x, xs') => (x==element) || listContains(xs', element)
}   



lemma appendExists<T>(xs:List<T>, ys:List<T>, element:T)
ensures listContains(append(xs, ys), element) ==  (listContains(xs, element) || listContains(ys, element))
{
    match(xs)
    case Nil => { }
    case Cons(x,xs') => {
        assert
            listContains(append(xs, ys), element) 

            == listContains(Cons(x, append(xs', ys)), element) 

            == listContains(xs, element) || listContains(ys, element) ;
        
    }
}


lemma sameElements<T>(tree:Tree<T>, element:T)
ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
{   
    match(tree)
    case Leaf => {}
    case Node(LTree, RTree, value) => {
         {appendExists(flatten(LTree), append(Cons(value, Nil), flatten(RTree)), element);}
        assert  treeContains(tree, element) 

            == treeContains(Node(LTree, RTree, value), element) 
        
            == treeContains(LTree, element) || treeContains(RTree, element) || (value == element) 
        
            == listContains(flatten(LTree), element) || listContains(flatten(RTree), element) || (value == element) 

            == listContains(flatten(LTree), element) || listContains(Cons(value, flatten(RTree)), element) 

            == listContains(flatten(LTree), element) || listContains(append(Cons(value, flatten(RTree)), Nil), element) 

            == listContains(flatten(LTree), element) || listContains(append(Cons(value, Nil), flatten(RTree)), element) 
            
            == listContains(append(flatten(LTree), append(Cons(value, Nil), flatten(RTree))), element) 
            
            == listContains(flatten(tree), element) ;
            
        }
    
}
