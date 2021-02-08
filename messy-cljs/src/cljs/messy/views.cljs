(ns messy.views
  (:require
   [re-frame.core :as re-frame]
   [reagent.core :as reagent]
   [messy.events :as events]
   [messy.subs :as subs]))

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
        recipient (re-frame/subscribe [::subs/recipient])
        message (re-frame/subscribe [::subs/content])]
    [:form {:on-submit (fn [e]
                         (.preventDefault e)
                         (re-frame/dispatch [::events/create-message @message @recipient @sender])
                         (re-frame/dispatch [::events/set-recipient ""])
                         (re-frame/dispatch [::events/set-content ""]))}
     [:div {:class "form-group"}
      [:label {:for "recipient"} "Recipient"]
      [:input {:name      "recipient"
               :class     "form-control"
               :type      "text"
               :value     @recipient
               :on-change #(re-frame/dispatch [::events/set-recipient (-> % .-target .-value .toLowerCase)])}]]
     [:div {:class "form-group"}
      [:label {:for "message"} "Message"]
      [:textarea {:name      "message"
                  :class     "form-control"
                  :value     @message
                  :on-change #(re-frame/dispatch [::events/set-content (-> % .-target .-value)])}]]
     [:button {:class "btn btn-primary "} "Send"]]))

(defn view-range-form []
  (let [range (re-frame/subscribe [::subs/range])
        begin_id (first @range)
        end_id (second @range)]
    [:form {:class     "form-inline"
            :on-submit #(do (.preventDefault %)
                            (re-frame/dispatch [::events/view-message-range begin_id end_id]))}
     [:label.sr-only {:for "start-id"} "Start id"]
     [:input.m-2 {:name        "start-id"
                  :style       {:width "10ch"}
                  :type        "text"
                  :placeholder "Start id"
                  :value       begin_id
                  :on-change   #(re-frame/dispatch [::events/set-range [(-> % .-target .-value) end_id]])}]
     [:label.sr-only {:for "start-id"} "End id"]
     [:input.m-2 {:name        "end-id"
                  :style       {:width "10ch"}
                  :type        "text"
                  :placeholder "End id"
                  :value       end_id
                  :on-change   #(re-frame/dispatch [::events/set-range [begin_id (-> % .-target .-value)]])}]
     [:button.btn.btn-primary "View range"]]))

(defn messages-options []
  [:div {:class "d-flex flex-row justify-content-around"}
   [:form
    [:button {:class    "btn btn-secondary"
              :on-click #(re-frame/dispatch [::events/view-new-messages])}
     "View new messages"]]
   (view-range-form)])

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
                [:th "Sent at"]]]
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
