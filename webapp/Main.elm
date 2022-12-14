module Main exposing (Model, Msg(..), pureFill, render, update, view)

-- non-obvious dependencies: elm/svg

import Array exposing (Array)
import Browser
import Html exposing (Html, br, button, div, input, span, table, td, text, th, tr)
import Html.Attributes as Attrs exposing (style, type_, value)
import Html.Events exposing (onClick, onInput)
import Svg
import Svg.Attributes as SAtt


xWIDTH : Int
xWIDTH =
    1024


main : Program () Model Msg
main =
    Browser.document { init = always init, update = update, view = view, subscriptions = \x -> Sub.batch [] }


type alias Model =
    { xis : Array Float
    , alpha : Float
    }


init =
    ( Model
        (Array.initialize 10 (\_ -> 1))
        0
    , Cmd.none
    )


type Msg
    = ChangeXi Int Float
    | ChangeAlpha Float
    | ChangeN Int
    | CheckAlpha
    | PureFill Int


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ChangeXi n f ->
            ( { model | xis = Array.set n f model.xis }, Cmd.none )

        ChangeAlpha f ->
            ( { model | alpha = f }, Cmd.none )

        ChangeN n ->
            ( { model
                | xis = newXis model.xis n
              }
            , Cmd.none
            )

        CheckAlpha ->
            ( { model
                | alpha = checkA model
              }
            , Cmd.none
            )

        PureFill n ->
            ( { model
                | xis = pureFill n (Array.length model.xis)
              }
            , Cmd.none
            )



-- checks the xis for the scattering condition, returning 0 if we're
-- all good, or the lowest x_i that kills it otherwise


checkA : Model -> Float
checkA model =
    -- strategy: make an array of the "sum if alpha started at each xi; return the xi of the index of the first >= 1
    let
        a : Array Float
        a =
            Array.map
                (\i ->
                    Array.foldr (+)
                        0
                        (Array.filter
                            (\x ->
                                (i <= x)
                                    && (x < 2 * i)
                            )
                            model.xis
                        )
                )
                model.xis

        -- p is alpha where alpha is biggest
        t : ( Int, Float )
        t =
            Array.foldl
                (\( i1, a1 ) ( i2, a2 ) ->
                    if a1 >= a2 then
                        ( i1, a1 )

                    else
                        ( i2, a2 )
                )
                ( 0, 0 )
                (Array.indexedMap (\n i -> ( n, i ))
                    a
                )

        p =
            Tuple.first t

        al =
            Tuple.second t
    in
    if al <= 1 then
        0

    else
        Maybe.withDefault 0 (Array.get p model.xis)


pureFill : Int -> Int -> Array Float
pureFill n m =
    let
        pureFillH : Int -> Int -> Int -> Array Float
        -- a : number of points
        -- b : base
        -- c : exponent
        pureFillH a b c =
            if a < (b * (2 ^ c)) then
                Array.repeat a (1 / toFloat (b * (2 ^ c)))

            else
                Array.append
                    (Array.repeat (b * (2 ^ c)) (1 / toFloat (b * (2 ^ c))))
                    (pureFillH
                        (a - (b * (2 ^ c)))
                        b
                        (c + 1)
                    )

        firstPointsH b c =
            -- b : base
            -- c : exponent
            if 2 ^ (c + 1) > b then
                Array.fromList []

            else
                Array.append
                    (Array.repeat (2 ^ c) (1 / toFloat (2 ^ c)))
                    (firstPointsH b (c + 1))

        firstPoints =
            firstPointsH n 0
    in
    Array.append
        firstPoints
        (pureFillH (m - Array.length firstPoints) n 0)



-- Sets the array a to a new size, n, by either truncating the end or appending to the end


newXis : Array Float -> Int -> Array Float
newXis a n =
    let
        m =
            Array.length a
    in
    if n == m then
        a

    else if n > m then
        Array.append a (Array.repeat (n - m) 1)

    else
        Array.slice 0 n a


view model =
    Browser.Document
        "18.821"
        [ changeN model
        , sumprod model
        , checkAlpha
        , strategies
        , render model
        , table [ style "width" "100%" ]
            (makeSliderAlpha model.alpha
                :: Array.toList
                    (Array.indexedMap
                        makeSliderXi
                        model.xis
                    )
            )
        ]


render : Model -> Html Msg
render model =
    Svg.svg
        [ style "border" "3px solid black"
        , SAtt.width (String.fromInt xWIDTH)
        , SAtt.height "50"
        , SAtt.viewBox ("0 0 " ++ String.fromInt xWIDTH ++ " 50")
        ]
        (List.concat
            [ [ Svg.rect
                    [ SAtt.x (String.fromInt (floor (model.alpha * toFloat xWIDTH)))
                    , SAtt.y "0"
                    , SAtt.width (String.fromInt (floor (model.alpha * toFloat xWIDTH)))
                    , SAtt.height "50"
                    , SAtt.color "pink"
                    , SAtt.fill "pink"
                    ]
                    []
              ]
            , List.map
                (\xi ->
                    Svg.circle
                        [ SAtt.cx (String.fromInt (floor (xi * toFloat xWIDTH)))
                        , SAtt.cy "25"
                        , SAtt.r "4"
                        ]
                        []
                )
                (Array.toList model.xis)
            ]
        )


checkAlpha : Html Msg
checkAlpha =
    div []
        [ text "Check all alpha"
        , button [ onClick CheckAlpha ] [ text "check!" ]
        ]


strategies : Html Msg
strategies =
    div []
        [ text "Potential Strategies: "
        , span []
            [ text "pure fill by 1/2^n "
            , button [ onClick (PureFill 2) ] [ text "select" ]
            ]
        , span []
            [ text " pure fill by 1/3^n "
            , button [ onClick (PureFill 3) ] [ text "select" ]
            ]
        , span []
            [ text " pure fill by 1/5^n"
            , button [ onClick (PureFill 5) ] [ text "select" ]
            ]
        ]


changeN : Model -> Html Msg
changeN model =
    div []
        [ text "N: "
        , input
            [ value (String.fromInt (Array.length model.xis))
            , onInput (\s -> ChangeN (Maybe.withDefault 1 (String.toInt s)))
            ]
            []
        , button [ onClick (ChangeN (1 + Array.length model.xis)) ]
            [ text "+" ]
        , button [ onClick (ChangeN (max 1 (Array.length model.xis - 1))) ]
            [ text "-" ]
        ]


sumprod : Model -> Html Msg
sumprod model =
    div []
        [ let
            p =
                Array.foldr (*) 1 model.xis

            s =
                Array.foldr (+) 0 (Array.map (logBase 10) model.xis)
          in
          text
            ("product: "
                ++ String.fromFloat p
                ++ "(log_10 = "
                ++ String.fromFloat s
                ++ ")"
            )
        , br [] []
        , let
            s =
                Array.foldr (+)
                    0
                    (Array.filter
                        (\x ->
                            (model.alpha <= x)
                                && (x < 2 * model.alpha)
                        )
                        model.xis
                    )
          in
          span
            [ style "color"
                (if s <= 1 then
                    "green"

                 else
                    "red"
                )
            ]
            [ text
                ("Sum from ?? to 2??: "
                    ++ String.fromFloat s
                )
            ]
        ]


makeSliderXi : Int -> Float -> Html Msg
makeSliderXi n curValue =
    makeSliderZeroOne (ChangeXi n) (String.fromFloat curValue) (String.fromInt (n + 1))


makeSliderAlpha : Float -> Html Msg
makeSliderAlpha curValue =
    makeSliderZeroOne ChangeAlpha (String.fromFloat curValue) "??"


makeSliderZeroOne : (Float -> Msg) -> String -> String -> Html Msg
makeSliderZeroOne fmsg curValue label =
    tr []
        [ td [] [ text (label ++ ": ") ]
        , td [ style "width" "75%" ]
            [ input
                [ type_ "range"
                , Attrs.min "0"
                , Attrs.max "1"
                , Attrs.step "any"
                , style "width" "100%"
                , value curValue
                , onInput (\s -> fmsg (Maybe.withDefault 0 (String.toFloat s)))
                ]
                []
            ]
        , td []
            [ input
                [ onInput (\s -> fmsg (Maybe.withDefault 0 (String.toFloat s)))
                , value curValue

                --, style "width" "20%"
                ]
                []
            ]
        ]
