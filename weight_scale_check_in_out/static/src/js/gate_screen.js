/** @odoo-module **/

import {registry} from '@web/core/registry';
import {useService} from "@web/core/utils/hooks";
const Dialog = require('web.Dialog');

const {Component, onWillStart,useState} = owl;
var session = require('web.session');

class TruckInOutComponent extends Component {
    setup() {
        this.orm = useService('orm');
        this.action = useService("action");
        this.state = useState({
        userId: null,
        userName: '',
        userImage: '',
        track_in:false,
        track_out:false,
        })
        onWillStart(async () => {
         const userData = await this.fetchCurrentUser();
            this.state.userId = userData.id;
            this.state.userName = userData.name;
            this.state.userImage = userData.image_1920;

            this.state.track_in = await session.user_has_group('weight_scale_check_in_out.track_in');
            this.state.track_out =await session.user_has_group('weight_scale_check_in_out.track_out');
        });
    }

    async fetchCurrentUser() {
        const currentUserId = session.uid;


        const user = await this.orm.read('res.users', [currentUserId], ['id', 'name', 'image_1920',]);
        return user[0];
    }

    async fetchWeight(url, options) {
        try {
            const response = await fetch(url, options);
            const data = await response.json();
            return data;
        } catch (error) {
            throw error;
        }
    }

    async getUrlData(userId) {
        const data = await this.orm.searchRead('gate.ip.address',
            [['user.id', '=', userId]], ['ip_address', 'port']);
        if (data.length === 0) {
            throw "Ip address configuration not found for current user."
        }
        const {ip_address, port} = data[0]
        let url = `http://127.0.0.1:65432?ip=${ip_address}&port=${port}`;
        let options = {
            method:"GET",
        };
        return {url, options}
    }

    handleError(error) {
        Dialog.alert(this, error);
    }


    async truckInOnClick() {
        try {
            const form_view = await this.orm.call('truck.check.in.check.out', 'get_form_view')
            const {url, options} = await this.getUrlData(this.state.userId);
            const result = await this.fetchWeight(url, options)
            if (result.status === 'success') this.showTruckInForm(form_view, result);
            if (result.status === 'fail') {
                throw result.error.exception;
            }
        } catch (error) {
            this.handleError(error);
        }
    }

    async truckOutOnClick() {
        try {
            const {url, options} = await this.getUrlData(this.state.userId);
            const result = await this.fetchWeight(url, options)
            if (result.status === 'success') this.showTruckOutForm(false, result);
            if (result.status === 'fail') {
                throw result.error.exception;
            }
        } catch (error) {
            this.handleError(error);
        }
    }

    showTruckInForm(view, data) {
        return this.action.doAction({
            res_model: 'truck.check.in.check.out',
            name: 'Truck IN',
            type: "ir.actions.act_window",
            views: [[view, "form"]],
            view_mode: "form",
            target: "new",
            context: {
                default_check_in_weight: data.weight,
            },
        }, {
            onClose: async () => {
                console.log('Closed')
            },
        });
    }

    showTruckOutForm (view, data) {
        return this.action.doAction({
            res_model: 'truck.out.finder',
            name: 'Truck Out',
            type: "ir.actions.act_window",
            views: [[view, "form"]],
            view_mode: "form",
            target: "new",
            context: {
                check_out_weight: data.weight,
            },
        }, {
            onClose: async () => {
                console.log('Closed')
            },
        });
    }
}

TruckInOutComponent.template = 'weight_scale_check_in_out.TruckCheckInOutButtons';

registry.category('actions').add('truck_check_in_out_gate', TruckInOutComponent);

export default TruckInOutComponent;
