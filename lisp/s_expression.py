klasa koja predstavlja s-expression
i lista i sam string su s-expression

interni data da je ili str ili nested tuple S expressiona

da ima fromStrTuple method koji prihvata izlaz parsera i vraća S kao prelazno
rešenje.
Prvo vidi kako će da se uklopi u eval, a onda napravi direktan parser za S

ima lep quote handling

ima isAtom, isNil i __eq__ __hash__ implementirano, 
kao i razne potrebne konstruktore i __iter__

