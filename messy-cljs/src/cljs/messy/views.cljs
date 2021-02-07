(ns messy.views
  (:require
    [re-frame.core :as re-frame]
    [reagent.core :as reagent]
    [messy.events :as events]
    [messy.subs :as subs]
    ))


(defn username-form []
      (let [username (re-frame/subscribe [::subs/username])]
           [:div
            [:input {:name        "username"
                     :class       "form-control"
                     :type        "text"
                     :placeholder "Username"
                     :value       @username
                     :on-change   #(re-frame/dispatch [::events/set-username (-> % .-target .-value)])}]]))

(defn message-form []
      (let [sender (re-frame/subscribe [::subs/username])
            recipient (reagent/atom "")
            message (reagent/atom "")]
           [:form {:on-submit (fn [e]
                                  (.preventDefault e)
                                  (re-frame/dispatch [::events/create-message @message @recipient @sender])
                                  (.reset (.-target e))
                                  (reset! recipient "")
                                  (reset! message ""))}
            [:div {:class "form-group"}
             [:label {:for "recipient"} "Recipient"]
             [:input {:name      "recipient"
                      :class     "form-control"
                      :type      "text"
                      :on-change #((do
                                     (reset! recipient (-> % .-target .-value .toLowerCase))))

                      }]]
            [:div {:class "form-group"}
             [:label {:for "message"} "Message"]
             [:textarea {:name      "message"
                         :class     "form-control"
                         :on-change #((do
                                        (reset! message (-> % .-target .-value))))

                         }]]
            [:button {:class "btn btn-primary "} "Send"]
            ]))

(defn messages-options []
      [:div {:class "d-flex flex-row"}
       [:button {:class    "btn btn-secondary"
                 :on-click #(re-frame/dispatch [::events/view-new-messages])
                 }
        "View new"]
       ])

(defn render-message [message]
      ^{:key (:id message)}
      [:tr
       [:th (:id message)]
       [:th (:sender message)]
       [:th (:recipient message)]
       [:th (:content message)]
       [:th (:created_at message)]
       [:th
        [:button {:type     "button"
                  :class    "btn btn-sm btn-danger"
                  :on-click #(re-frame/dispatch [::events/delete-message (:id message)])}
         "Delete"]]])

(defn messages []
      (let [messages (re-frame/subscribe [::subs/messages])]
           (when (seq @messages)
                 [:table {:class "table"}
                  [:thead [:tr
                           [:th "Id"]
                           [:th "Sender"]
                           [:th "Recipient"]
                           [:th "Message"]
                           [:th "Sent at"]
                           ]]
                  [:tbody (map render-message @messages)]])))

(defn main-panel []
      [:div {:class "container mt-4"}
       [:div {:class "d-flex flex-row justify-content-between"}
        [:h1 "Welcome to Messy"]
        (username-form)]
       (messages-options)
       (messages)
       [:hr]
       [:div {:class "container"}
        (message-form)]])